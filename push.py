from os import system
for i in ['git status', 'git diff', 'git add .', f'git commit -m "{input("Enter the comment message > ")}"', 'git push -u origin master']: system(i)
