
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views import View

from .models import Stage, Task, TaskSolution
from .task_executor import TaskExecutor


class LoginRequiredBaseView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'


class StagesView(LoginRequiredBaseView):

    def get(self, request, *args, **kwargs):
        return self.render_stages(request)

    def post(self, request, *args, **kwargs):
        return self.render_stages(request)

    def render_stages(self, request):
        all_stages = Stage.objects.all().order_by('difficulty')
        return render(request, 'stages.html', {'stages': all_stages})


class StageView(LoginRequiredBaseView):

    def get(self, request, name, *args, **kwargs):
        return self.render_stage(request, name)

    def post(self, request, name, *args, **kwargs):
        return self.render_stage(request, name)

    def render_stage(self, request, name):
        user = request.user
        stage = get_object_or_404(Stage, name=name)
        all_levels = Task.objects.filter(stage=stage).order_by('level')
        solved_levels = Task.objects.filter(
            stage=stage,
            task_solutions__in=TaskSolution.objects.filter(user=user, solved=True)
        )
        return render(request, 'levels.html', {'stage': stage, 'levels': all_levels, 'solved_levels': solved_levels})


class TaskView(LoginRequiredBaseView):

    def get(self, request, id, *args, **kwargs):
        assert request.user.is_authenticated
        task = get_object_or_404(Task, id=id)
        task_solution, _ = TaskSolution.objects.get_or_create(task=task, user=request.user)
        registers_list = self.get_registers_list(task)
        return render(request, 'task_cards.html', {
            'task': task,
            'code': task_solution.code,
            'registers_list': registers_list,
        })

    def post(self, request, id, *args, **kwargs):
        context = {}
        task = get_object_or_404(Task, id=id)
        context['task'] = task
        task_solution, _ = TaskSolution.objects.get_or_create(task=task, user=request.user)
        if request.POST.has_key('code') and request.POST['code']:
            code = request.POST['code'].replace("\r", "")
            context['code'] = code
            task_solution.code = code
            task_executor = TaskExecutor(task)
            try:
                task_executor.execute(code)
                context['register_values_list'] = task_executor.get_actual_registers()
                context['solved'] = task_executor.was_successful()
                if not task_solution.solved and context['solved']:
                    task_solution.solved = True
            except Exception as e:
                context['error'] = str(e)
            task_solution.save()
        else:
            context['code'] = task_solution.code
        context['registers_list'] = self.get_registers_list(task, context.get('register_values_list'))
        return render(request, 'task_cards.html', context)

    def get_registers_list(self, task, actual_registers_list=None):
        assert len(task.initial_register_list) == len(task.expected_register_list)
        if actual_registers_list:
            assert len(actual_registers_list) == len(task.initial_register_list)
        registers_list = []
        for i in range(len(task.initial_register_list)):
            registers_list.append([
                task.initial_register_list[i],
                task.expected_register_list[i],
                None if not actual_registers_list else actual_registers_list[i]
            ])
        return registers_list