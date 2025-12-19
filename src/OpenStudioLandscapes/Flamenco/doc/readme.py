import textwrap

import snakemd


def readme_feature(
        doc: snakemd.Document,
        main_header: str,
) -> snakemd.Document:

    # Some Specific information

    doc.add_heading(
        text=main_header,
        level=1,
    )

    # Logo

    doc.add_paragraph(
        snakemd.Inline(
            text=textwrap.dedent(
                """\
                Logo Flamenco\
                """
            ),
            image="https://flamenco.blender.org/brand.svg",
            link="https://flamenco.blender.org/",
        ).__str__()
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """\
            Official Flamenco information.\
            """
        )
    )

    doc.add_heading(
        text="Quickstart",
        level=2,
    )

    doc.add_unordered_list(
        [
            "[Quickstart](https://flamenco.blender.org/usage/quickstart/)",
        ]
    )

    doc.add_heading(
        text="Help",
        level=2,
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """\
            Remember to add flamenco-manager FQDN to
            your local DNS server for the worker to be able
            to find it by.\
            """
        )
    )

    doc.add_heading(
        text="Manager",
        level=3,
    )

    doc.add_code(
        textwrap.dedent(
            """\
            ./flamenco-manager --help                                                                                                                                                                                                              ✔ 
            2025-10-29T13:04:02+01:00 INF starting Flamenco arch=amd64 git=72c1bad4 os=linux osDetail="Manjaro Linux (6.16.8-1-MANJARO)" releaseCycle=release version=3.7
            Usage of ./flamenco-manager:
              -debug
                    Enable debug-level logging.
              -delay
                    Add a random delay to any HTTP responses. This aids in development of Flamenco Manager's web frontend.
              -pprof
                    Expose profiler endpoints on /debug/pprof/.
              -quiet
                    Only log warning-level and worse.
              -setup-assistant
                    Open a webbrowser with the setup assistant.
              -trace
                    Enable trace-level logging.
              -version
                    Shows the application version, then exits.
              -write-config
                    Writes configuration to flamenco-manager.yaml, then exits.\
"""
        )
    )

    doc.add_unordered_list(
        [
            "[Manager Configuration](https://flamenco.blender.org/usage/manager-configuration/)",
        ]
    )

    doc.add_heading(
        text="Worker",
        level=3,
    )

    doc.add_code(
        textwrap.dedent(
            """\
            ./flamenco-worker --help                                                                                                                                                                                                               ✔ 
            Usage of ./flamenco-worker:
              -debug
                    Enable debug-level logging.
              -find-manager
                    Autodiscover a Manager, then quit.
              -flush
                    Flush any buffered task updates to the Manager, then exits.
              -manager string
                    URL of the Flamenco Manager.
              -quiet
                    Only log warning-level and worse.
              -register
                    (Re-)register at the Manager.
              -restart-exit-code int
                    Mark this Worker as restartable. It will exit with this code to signify it needs to be restarted.
              -trace
                    Enable trace-level logging.
              -version
                    Shows the application version, then exits.\
"""
        )
    )

    doc.add_unordered_list(
        [
            "[Worker Configuration](https://flamenco.blender.org/usage/worker-configuration/)",
        ]
    )

    doc.add_code(
        textwrap.dedent(
            """\
            ./flamenco-worker -manager flamenco-manager.openstudiolandscapes.lan:8484                                                                                                                                                              ✔ 
            2025-10-29T15:30:42+01:00 INF starting Flamenco Worker arch=amd64 git=72c1bad4 os=linux osDetail="Manjaro Linux (6.16.8-1-MANJARO)" pid=625742 releaseCycle=release version=3.7
            2025-10-29T15:30:42+01:00 INF will load configuration from these paths credentials=/home/michael/.local/share/flamenco/flamenco-worker-credentials.yaml main=/home/michael/Downloads/flamenco-3.7-linux-amd64/flamenco-worker.yaml
            2025-10-29T15:30:42+01:00 INF using Manager URL from commandline manager=http://flamenco-manager.openstudiolandscapes.lan:8484
            2025-10-29T15:30:42+01:00 INF Blender could not be found. Flamenco Manager will have to supply the full path to Blender when tasks are sent to this Worker. For more info see https://flamenco.blender.org/usage/variables/blender/
            2025-10-29T15:30:42+01:00 INF FFmpeg found on this system path=/home/michael/Downloads/flamenco-3.7-linux-amd64/tools/ffmpeg-linux-amd64 version=7.0.2-static
            2025-10-29T15:30:42+01:00 INF loaded configuration config={"ConfiguredManager":"","LinuxOOMScoreAdjust":null,"ManagerURL":"http://flamenco-manager.openstudiolandscapes.lan:8484","RestartExitCode":0,"TaskTypes":["blender","ffmpeg","file-management","misc"],"WorkerName":""}
            2025-10-29T15:30:42+01:00 INF loaded credentials filename=/home/michael/.local/share/flamenco/flamenco-worker-credentials.yaml
            2025-10-29T15:30:42+01:00 INF signing on at Manager manager=http://flamenco-manager.openstudiolandscapes.lan:8484 name=lenovo softwareVersion=3.7 taskTypes=["blender","ffmpeg","file-management","misc"]
            2025-10-29T15:30:42+01:00 WRN unable to sign on at Manager code=403 resp={"code":0,"message":"Security requirements failed"}
            2025-10-29T15:30:42+01:00 INF registered at Manager code=200 resp={"address":"192.168.178.195","name":"lenovo","platform":"linux","software":"","status":"","supported_task_types":["blender","ffmpeg","file-management","misc"],"uuid":"73f5de82-a3aa-4f93-ab88-b3adf0be35d6"}
            2025-10-29T15:30:42+01:00 INF Saved configuration file filename=/home/michael/.local/share/flamenco/flamenco-worker-credentials.yaml
            2025-10-29T15:30:42+01:00 INF signing on at Manager manager=http://flamenco-manager.openstudiolandscapes.lan:8484 name=lenovo softwareVersion=3.7 taskTypes=["blender","ffmpeg","file-management","misc"]
            2025-10-29T15:30:42+01:00 INF manager accepted sign-on startup_state=awake
            2025-10-29T15:30:42+01:00 INF opening database dsn=/home/michael/.local/share/flamenco/flamenco-worker.sqlite
            2025-10-29T15:30:42+01:00 INF state change curState=starting newState=awake
            ^C2025-10-29T15:30:49+01:00 INF signal received, shutting down. signal=interrupt
            2025-10-29T15:30:49+01:00 INF signing off at Manager state=offline
            2025-10-29T15:30:49+01:00 WRN shutdown complete, stopping process.\
"""
        )
    )

    return doc


if __name__ == "__main__":
    pass
