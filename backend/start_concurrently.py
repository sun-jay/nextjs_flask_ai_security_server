import subprocess

# Define the commands to be executed

processes = {
    'app.py':[
        'cd C:\\Security Cam Proj\\nextjs_flask_ai_security_server\\backend',
        'python app.py',
    ],
    'manage_vid_files_and_logs.py':[
        'cd C:\\Security Cam Proj\\nextjs_flask_ai_security_server\\backend',
        'python manage_vid_files_and_logs.py',
    ],
    'run_ffmpeg.py':[
        'cd C:\\Security Cam Proj\\nextjs_flask_ai_security_server\\backend\\saved_streams',
        'python test.py',
    ],
    'person_detect.py':[
        'cd C:\\Security Cam Proj\\nextjs_flask_ai_security_server\\backend',
        'python person_detect.py',
    ],
    'frontend':[
        'cd C:\\Security Cam Proj\\nextjs_flask_ai_security_server\\backend',
        'npm run dev',
    ]
}

current_processes = []
for process in processes:
    for line in processes[process]:
        proc = subprocess.Popen(['start', 'cmd', '/c', f'title {process} && {line}'], shell=True)

        current_processes.append(proc)

while True:
    input('Press enter to exit\n')
    for proc in current_processes:
        proc.terminate()
    break

        
    
