from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

class M1(MiddlewareMixin):
    """中间件1"""
    def process_request(self,request):
        #排除那些不需要登录就能访问的页面
        #request.path.info 获取当前用户的请求url
        if request.path_info in ['/login','/image/code/']:
            return
        info = request.session.get("info")
        print(info)
        if info:
            return
        return redirect('/login')
        #如果没有返回值，则返回None
        #如果有返回值，则请求返回
    # def prcess_response(self,request,response):
    #     return

