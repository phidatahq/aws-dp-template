from phidata.app.assistant import Assistant

from workspace.settings import ws_settings

#
# -*- Assistant Docker resources
#

dev_assistant = Assistant(
    enabled=ws_settings.dev_assistant_enabled, container_host_port=9090
)
