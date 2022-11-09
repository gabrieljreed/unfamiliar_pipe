import pipe.pipeHandlers.element as Element
import pipe.pipeHandlers.environment as Environment
import os

env = Environment.Environment()
shot_dir = env.get_shot_dir()
shot_dir_list = os.listdir(shot_dir)
print('SHOTS CHECKED OUT:\n')
for dir in shot_dir_list:
    el_path = shot_dir + '/' + dir + '/' + '.element'
    if os.path.exists(el_path):
        el = Element.Element(el_path)
        user = el.get_assigned_user()
        if user != '':
            print(dir + ': ' + user)