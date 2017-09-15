from django.views.generic import View
from django.contrib.auth.models import User,Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import  HttpResponse,JsonResponse,QueryDict
from django.db.models import  Q
from accounts.mixins import myPermissionRequiredMixin

class MOdifyUserStatusView(LoginRequiredMixin,View):

    def post(self,request):

        uid=request.POST.get('uid')
        ret = {"status":0}
        try:
            user_obj = User.objects.get(id=uid)
            user_obj.is_active = False if user_obj.is_active else True
            user_obj.save()
            ret["errmsg"] = "用户状态已经更改666！"
        except User.DoesNotExist as e:
            ret["status"] = 1
            ret["errmsg"] ="用户不存在！"
        return JsonResponse(ret)

    #从组中删除用户
    def delete(self,request):
        if not request.user.has_perm('auth.delete_group_users'):
            res = {"status": 1}
            res["errmsg"] = "你没有从用户组删除用户的权限。"
            return JsonResponse(res, safe=False)
        res = {'status':0}
        data = QueryDict(request.body)
        uid =data.get("uid","")
        gid =data.get("gid","")
        # print("{0},{1}".format(uid,gid))
        try:
            u_obj = User.objects.get(id=uid)
            g_obj = Group.objects.get(id=gid)
            u_obj.groups.remove(g_obj)
            res['errmsg'] = "用户 [ {0} ] 已经从组 [ {1} ] 中删除 666".format(u_obj.username,g_obj.name)
        except User.DoesNotExist:
            res['status'] = 1
            res['errmsg'] = "用户不存在！"
        except Group.DoesNotExist:
            res['status'] = 1
            res['errmsg'] = "用户组不存在"
        except:
            res['status'] = 1
            res['errmsg'] = "从组中移除用户失败"
        return JsonResponse(res,safe=False)




class MOdifyGroupView(LoginRequiredMixin,View):
    def get(self,request):
        groups = list( Group.objects.all().values('id','name'))
        return JsonResponse(groups,safe=False)




class UserGroupListView(LoginRequiredMixin,View):

    def get(self,request):
        res = {"status": 1}
        uid  = request.GET.get("uid")
        try:
            u = User.objects.get(id=uid)
            ug = u.groups.all().values_list('id')
            if ug:
                res = Group.objects.all().exclude(id__in=ug).values('id','name')
            else:
                res = Group.objects.all().values('id', 'name')
        except User.DoesNotExist as e:
            res["errmsg"] = "用户不存在啊！"
        except Exception as e:
            res["errmsg"] =  e.args
        print (res)
        return  JsonResponse(list(res),safe=False)

    def put(self,request):
        if not request.user.has_perm('auth.add_user_group'):
            res = {"status": 1}
            res["errmsg"] = "你真没有添加用户到用户组的权限。"
            return JsonResponse(res,safe=False)
        data = QueryDict(request.body)
        uid  = data.get('uid','')
        gid  = data.get('gid','')
        print("{0}:{1}".format(uid,gid))
        res = {'status':0}
        try:
            u = User.objects.get(id=uid)
            g = Group.objects.get(id=gid)
            u.groups.add(g)
            res['errmsg'] ='已经添加到用户组！'
        except:
            res['status'] = 1
            res['errmsg'] ='用户添加用户组失败！'
        return  JsonResponse(res,safe=False)





