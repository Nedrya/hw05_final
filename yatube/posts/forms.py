from django import forms
from .models import Post
from .models import Comment


#  создадим собственный класс для формы регистрации
#  сделаем его наследником предустановленного класса UserCreationForm
class PostForm(forms.ModelForm):
    class Meta:
        # укажем модель, с которой связана создаваемая форма
        model = Post
        # укажем, какие поля должны быть видны в форме и в каком порядке
        fields = ('text', 'group', 'image')


class CommentForm(forms.ModelForm):
    class Meta:
        # укажем модель, с которой связана создаваемая форма
        model = Comment
        # укажем, какие поля должны быть видны в форме и в каком порядке
        fields = ('text',)
