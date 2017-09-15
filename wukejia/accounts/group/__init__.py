from django.contrib.auth.models import Group, User,Permission,ContentType
from django.http import JsonResponse, QueryDict, Http404,HttpResponseRedirect,HttpResponse
from django.views.generic import ListView, View, TemplateView
from django.shortcuts import redirect,reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.mixins import myPermissionRequiredMixin


class GroupListView(LoginRequiredMixin,ListView):
    model =  Group
    template_name = "user/grouplist.html"


class GroupCreateView(LoginRequiredMixin,View):

    def post(self,request):
        if not request.user.has_perm('auth.add_group'):
            res = {"status": 1}
            res["errmsg"] = "你真没有增加用户组的权限，跳过前端没用的。"
            return JsonResponse(res,safe=False)
        res = {"status": 0}
        group_name=request.POST.get("group_name")
        if group_name:
            try:
                g =  Group(name=group_name)
                g.save()
                res["errmsg"]="群组:{0} 添加成功！".format(group_name)
            except Exception as e:
                res["status"] = 1
                res["errmsg"] = e.args
        else:
            res["status"]=1
            res["errmsg"]="用户名参数有误！"
        return  JsonResponse(res,safe=False)

    def delete(self,request):
        if not request.user.has_perm('auth.delete_group'):
            res = {"status": 1}
            res["errmsg"] = "你真没有删除用户组的权限，跳过前端没用的。"
            return JsonResponse(res,safe=False)
        res = {"status": 0}
        gid = QueryDict(request.body).get('gid')
        #查验是否组内有权限有则不删除。
        g_allp_num=0
        try:
            g = Group.objects.get(id=gid)
            g_allp_num = len(g.permissions.all())
            if not g_allp_num == 0:
                res['status'] = 1
                res['errmsg'] = "群组 [ {1}] 分配有 [ {0} ] 个权限,不能删除。".format(g_allp_num,g.name)
                return JsonResponse(res, safe=False)
        except Exception as e:
            res['status']=1
            res['errmsg']=e.args
            return JsonResponse(res, safe=False)

        #查验是否有用户在 组内，有则报告数目，不删除
        user_nums = User.objects.filter(groups__id=gid).count()
        if user_nums != 0:
            res = {"status": 1}
            res['errmsg'] = "群组下还有 [ {0} ] 个用户,不能删除。".format(user_nums)
            return JsonResponse(res,safe=False)
        try:
            g = Group.objects.get(id=gid)
            g.delete()
            res['errmsg']="群组 {0} 已经删除！".format(g.name)
        except Group.DoesNotExist as e:
            res['status']=1
            res['errmsg']="删除失败，群组不存在！{0}".format(g.name)
        except:
            res['status']=1
            res['errmsg']="原因未知！{0}".format(g.name)
        return  JsonResponse(res,safe=False)



class GroupUserList(LoginRequiredMixin,myPermissionRequiredMixin,TemplateView):
    permission_required = 'auth.view_group_users'
    next_path = 'group_list'
    msg = '你没有查看用户组下用户列表的权限，请老实的联系管理员吧。'

    template_name = 'user/group_userlist.html'
    def get_context_data(self, **kwargs):
        context = super(GroupUserList, self).get_context_data(**kwargs)
        #self.request 是一个参数 在as_view里面定义 不是request对象
        gid = self.request.GET.get("gid", "")
        print(gid)
        try:
            g_obj = Group.objects.get(id = gid)
            context['object_list'] = g_obj.user_set.all()
            context['gid'] = gid
        except Group.DoesNotExist:
            raise Http404("the group is not exist !")
        except:
            pass

        return context









class ModifyGroupPermissionList(LoginRequiredMixin,myPermissionRequiredMixin,TemplateView):
    permission_required = 'auth.change_group_permission'
    next_path = 'group_list'
    msg = '你没有更改用户组权限的权限，请老实的联系管理员吧。'

    template_name = 'user/modify_group_permissions.html'

    def get_context_data(self, **kwargs):
        context = super(ModifyGroupPermissionList, self).get_context_data(**kwargs)
        context['contenttypes'] = ContentType.objects.all()
        context['group'] = self.request.GET.get("gid","")
        context['group_permissions'] = self.get_group_permission(context['group'])
        # try:
        #     g = Group.objects.get(pk=gid)
        #     getid_tuple = g.permissions.all().values_list('id')
        #     group_permissions_list=[]
        #     for i in list(getid_tuple):
        #         group_permissions_list.append(i[0])
        #     context['group_permissions']=group_permissions_list
        #     # print(group_permissions_list)
        # except Exception as e:
        #     return redirect('error','group_list',e.args)
        return  context

    def get_group_permission(self,groupid):
        try:
            group_obj = Group.objects.get(pk=groupid)
            all_permissons = group_obj.permissions.all()
            # print ( [ i.id for i in all_permissons])
            #666
            return  [ i.id for i in all_permissons]
        except Group.DoesNotExist :
            return redirect('error',next='group_list',msg="用户组不存在")


    def post(self,request):
        res = {"status":0}
        permission_id_list = request.POST.getlist("permission",[])
        groupid = request.POST.get("groupid","")
        try:
            g = Group.objects.get(pk=groupid)
        except Exception as e:
            return redirect('error',next='group_list',msg='用户组不存在！')

        try:
            permission_query = Permission.objects.filter(id__in=permission_id_list)
            g.permissions.set(permission_query)
            gourl = reverse("group_permission_modify")
            gourl = gourl +"?gid="+groupid
            return HttpResponseRedirect(gourl)
        except Exception as e:
            return redirect('error','group_list',e.args)



class showGroupPermission(LoginRequiredMixin,myPermissionRequiredMixin,TemplateView):
    permission_required = 'auth.view_group_permission'
    next_path = 'group_list'
    msg = '您没有查看用户组权限列表的权限，请联系管理员吧，啊。'

    template_name = 'user/show_group_permissions.html'
    def get_context_data(self, **kwargs):
        context = super(showGroupPermission, self).get_context_data(**kwargs)
        gid = self.request.GET.get("gid","")


        try:
            group_obj =  Group.objects.get(pk=gid)
            group_query = Group.objects.filter(id=gid).values('name')
            context['group_mingzi'] = list(group_query)[0]['name']
            context['object_list']=group_obj.permissions.all()

            print(context['group_mingzi'] )
        except Group.DoesNotExist as e:
            return redirect('error','group_list',e.args)
        except Exception as f:
            return redirect('error','group_list',f.args)
        return  context
