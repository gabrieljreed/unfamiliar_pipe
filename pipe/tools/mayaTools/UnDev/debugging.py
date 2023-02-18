"""
-------------------------------------------------- DEBUGGING IN UNMAYA -------------------------------------------------

Start a debug session by clicking the "Debug" button in the UnMaya UI. This will freeze Maya until a debugger is 
attached. Once Maya is frozen and you see the prompt "Waiting for debugger to attach...", open VS Code and make sure 
you have a launch.json file in your workspace. 

NOTE: If you open the anim_pipeline workspace, you will already have a launch.json file
(open this filepath in VS Code as your workspace: /groups/unfamiliar/anim_pipeline)

If you don't have one, you can create one by clicking the "Add Configuration" button in the debug tab. Once you have a
 launch.json file, replace the contents with the following:

{
    "version": "0.2.0",
    "configurations": [

        {
            "name": "Maya Python: Remote Attach",
            "type": "python",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": "${workspaceFolder}"
                }
            ],
            "justMyCode": true
        }
    ]
}

Once you have a launch.json file, click the "Debug" button in the debug tab. This will attach the debugger to the
debug session. You can now set breakpoints and debug your code.

"""


def start_debug_session():
    import os
    import pipe.tools.mayaTools.UnDev.debugpy as debugpy

    # Configure the debugger for Maya 
    print("Waiting for debugger to attach...")
    maya_location = os.path.join(os.environ['MAYA_LOCATION'], 'bin', 'mayapy')
    debugpy.configure({"python": maya_location})

    # Start a debug session
    debugpy.listen(5678)
    debugpy.wait_for_client()


class mayaRun:
    def run(self):
        start_debug_session()
