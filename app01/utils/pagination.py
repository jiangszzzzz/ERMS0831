"""
自定义分页组件 使用分页组件 需要完成后以下步骤

在视图函数中

def pretty_list(request):

    # 1 根据情况筛选数据
    queryset = models.PrettyNum.objects.all()

    # 2 实例化分页对象
    page_object = Pagination(request, queryset)

    context = {
        "queryset": page_object.page_queryset,  # 分完也的数据
        "page_string": page_object.html(),  # 页码
    }
    return render(request, "pretty_list.html", context)

在html中

        {% for obj in queryset %}
                <tr>
                    <td>{{ obj.id }}</td>
                </tr>
        {% endfor %}

        <ul class="pagination">
            {{ page_string }}
        </ul>

"""
from django.utils.safestring import mark_safe
import copy
from django.http.request import QueryDict


class Pagination(object):
    def __init__(self, request, query_set, page_size=10, page_param="page", plus=5):
        '''
        :param request: 请求的对象
        :param query_set:符合条件的数据（根据这个数据进行分页处理）
        :param page_size:每页显示多少条数据
        :param page_param:在URL中传递的获取分页的参数 利用 /pretty/list/?page=12
        :param plus: 显示当前页的前几页 后几页
        '''

        # 带上 url传入的参数 实现搜索分页
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        self.page_param = page_param

        # 没有传入get参数 则page 为 1
        page = request.GET.get(page_param, "1")

        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size

        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = query_set[self.start:self.end]

        # 统计数据库中的数据个数
        total_count = query_set.count()
        # 页码总数
        total_page_count, mod = divmod(total_count, page_size)
        if mod:
            total_page_count += 1
        self.total_page_count = total_page_count

        self.plus = plus

    def html(self):
        # 根据用户访问的页码，计算出起始页码位置

        # 显示当前页的前五页与后五页
        if self.total_page_count <= 2 * self.plus:
            # 数据库数据少
            start_page = 1
            end_page = self.total_page_count
        else:
            # 数据库数据多
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus
            else:
                if self.page + self.plus > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus + 1
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus + 1
                    end_page = self.page + self.plus
        # 页码
        page_str_list = []

        # 带上 url传入的参数 实现搜索分页
        self.query_dict.setlist(self.page_param, [1])

        # 首页
        firstv = '<li><a href="/pretty/list/?{}">首 页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(firstv)

        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="/pretty/list/?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li><a href="/pretty/list/?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        for i in range(start_page, end_page + 1):
            if i == self.page:
                self.query_dict.setlist(self.page_param, [i])
                ele = '<li class = "active"><a href="/pretty/list/?{}">{}</a></li>'.format(
                    self.query_dict.urlencode(), i)
            else:
                self.query_dict.setlist(self.page_param, [i])
                ele = '<li><a href="/pretty/list/?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        # 下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            nextv = '<li><a href="/pretty/list/?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            nextv = '<li><a href="/pretty/list/?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(nextv)

        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        lastv = '<li><a href="/pretty/list/?{}">尾 页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(lastv)

        '''
        <li><a href="/pretty/list/?page=1">1</a></li>
        <li><a href="/pretty/list/?page=2">2</a></li>
        <li><a href="/pretty/list/?page=3">3</a></li>
        <li><a href="/pretty/list/?page=4">4</a></li>
        <li><a href="?page=5">5</a></li>
        '''

        search_string = """
                   <li>
                       <form style="float: left;margin-left: -1px" method="get">
                           <input name="page"
                                  style="position: relative; float: left; display: inline-block;width: 100px;border-radius: 0px;"
                                  type="text" class="form-control" placeholder="页码">
                           <button style="border-radius: 0" class="btn btn-default" type="submit">跳转</button>
                       </form>
                   </li>
           """
        page_str_list.append(search_string)

        page_string = mark_safe("".join(page_str_list))
        return page_string
