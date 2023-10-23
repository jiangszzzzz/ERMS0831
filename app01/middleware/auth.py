from django.middleware.common import CommonMiddleware
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 排除不需要登录就能访问的页面
        # request.path_info 获取当前用户请求的 URL
        if request.path_info in ["/login/", "/image/code/"]:
            return

        # 读取当前用户请求的 session信息 如果能读到 就可以 return None， 既 继续走
        info_dict = request.session.get("info")
        # print(info_dict)

        if info_dict:
            return
        # 没登录过 重回登录页面
        return redirect("/login/")
