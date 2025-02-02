from django.shortcuts import render, redirect, HttpResponse
from web.forms.project import ProjectModelForm
from django.http import JsonResponse
from web import models


def project_list(request):
    '''项目列表'''
    if request.method == 'GET':
        # 查看项目
        project_dict = {'star': [], 'my': [], 'join': []}
        # 1 我创建的项目
        my_project_list = models.ProjectInfo.objects.filter(creator=request.tracer.user)
        # 2 我参与的项目
        join_project_list = models.ProjectTeamInfo.objects.filter(user=request.tracer.user)

        for row in my_project_list:
            if row.star:
                project_dict['star'].append({'value': row, 'type': 'my'})
            else:
                project_dict['my'].append(row)
        for item in join_project_list:
            if item.star:
                project_dict['star'].append({'value': item.project, 'type': 'join'})
            else:
                project_dict['join'].append(item.project)
        form = ProjectModelForm(request)
        return render(request, 'project_list.html', {'form': form, 'project_dict': project_dict})
    # 添加项目
    form = ProjectModelForm(request, data=request.POST)
    if form.is_valid():
        # 验证通过，只有三个字段，其他需要自己填，除了项目名称、颜色、描述 + 创建用户
        form.instance.creator = request.tracer.user
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def project_star(request, project_type, project_id):
    if project_type == 'my':
        models.ProjectInfo.objects.filter(id=project_id, creator=request.tracer.user).update(star=True)
        return redirect('project_list')
    if project_type == 'join':
        models.ProjectTeamInfo.objects.filter(project_id=project_id, user=request.tracer.user).update(star=True)
        return redirect('project_list')
    return HttpResponse('出错了')


def project_unstar(request, project_type, project_id):
    if project_type == 'my':
        models.ProjectInfo.objects.filter(id=project_id, creator=request.tracer.user).update(star=False)
        return redirect('project_list')
    if project_type == 'join':
        models.ProjectTeamInfo.objects.filter(project_id=project_id, user=request.tracer.user).update(star=False)
        return redirect('project_list')
    return HttpResponse('出错了')
