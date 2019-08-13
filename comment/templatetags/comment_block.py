from django import template
from comment.forms import CommentForm
from comment.models import Comment

# 固定写法，注册Library实例
register = template.Library()


@register.inclusion_tag('comment/block.html')
def comment_block(target):
	return {
		'target': target,
		'comment_form': CommentForm(initial={'nickname': '阳哥',
											 'email': '568726669@qq.com',
											 'website': 'http://www.baidu.com'}),
		'comment_list': Comment.get_by_target(target)
	}
