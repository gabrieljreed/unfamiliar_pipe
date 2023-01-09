import json
import pipe.pipeHandlers.environment as env

class RenderSettings:

    def __init__(self):
        e = env.Environment()
        json_path = e.project_dir + "/pipe/tools/houdiniTools/render/render_settings.json"

        with open(json_path) as f:
            self.render_settings = json.load(f)

    def getAOVs(self):
        return self.render_settings['AOVs']

    def getLayers(self):
        return self.render_settings['layers']