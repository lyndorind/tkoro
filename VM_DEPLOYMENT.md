# Lab 7 — separate VM with Docker Compose (Windows host)

**Important:** Windows Docker Desktop's internal WSL2 VM is **not** a substitute for the separate VM requested in the assignment. These steps require action on your Windows PC.

## 1. Create the virtual machine

Use Oracle VirtualBox (or Hyper-V if Windows edition supports it):

- Name: `Lab7-Ubuntu`
- Guest OS: Ubuntu Server 24.04 LTS, 64-bit
- CPU: 2 virtual cores
- Memory: 4 GiB
- Disk: dynamically allocated, **25 GiB or larger**
- Network: **NAT**
- Install Ubuntu and remember the guest username and password.

With the VM powered off, open **Settings → Network → Adapter 1 (NAT) → Advanced → Port Forwarding** and add:

| Name | Protocol | Host IP | Host port | Guest IP | Guest port |
| --- | --- | --- | --- | --- | --- |
| lab7-api | TCP | 127.0.0.1 | 18000 | (blank) | 8000 |

Use host port **18000** because Windows Docker Desktop already uses port 8000. Do not expose PostgreSQL port 5432 to the internet.

## 2. Install Git and Docker Engine inside Ubuntu VM

In the Ubuntu terminal:

```bash
sudo apt update
sudo apt install -y ca-certificates curl git
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

sudo tee /etc/apt/sources.list.d/docker.sources > /dev/null <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo docker --version
sudo docker compose version
```

This is based on the official Docker Engine installation procedure for Ubuntu: https://docs.docker.com/engine/install/ubuntu/ . The official docs take precedence if their commands change.

## 3. Clone your repository and create a separate VM secret

```bash
git clone https://github.com/lyndorind/tkoro.git
cd tkoro
git switch main

# Password is typed invisibly and stored only inside the VM (not Git).
umask 077
mkdir -p secrets
read -r -s -p 'Enter a new password for the VM database: ' lab7_vm_password
printf '\n'
printf '%s' "$lab7_vm_password" > secrets/db_password.txt
unset lab7_vm_password

sudo docker compose config --quiet
sudo docker compose up -d --build
sudo docker compose ps
```

If the service images need time to build, wait for completion. The `db` service should eventually show **healthy**, and the `api` service **running**. Do **not** run `docker compose down -v`: that deletes the database volume.

## 4. Verify requests, containers, logs and resource utilization

```bash
curl -i http://localhost:8000/health
curl -i -H 'Content-Type: application/json' \
  -d '{"text":"Lab 7 deployed on separate Ubuntu VM"}' \
  http://localhost:8000/notes

# Replace 1 with the id that POST returned (often 1 in a new VM database):
curl -i http://localhost:8000/notes/1

sudo docker compose ps
sudo docker inspect tkoro-api-1 --format '{{.Name}} {{.State.Status}} {{.Config.Image}}'
sudo docker inspect tkoro-db-1 --format '{{.Name}} {{.State.Health.Status}} {{.Config.Image}}'
sudo docker compose logs --tail=30 api
sudo docker compose logs --tail=30 db
sudo docker stats --no-stream tkoro-api-1 tkoro-db-1
```

Container names usually follow `tkoro-api-1` and `tkoro-db-1`; if they differ, get exact names from `sudo docker compose ps` and replace them in `docker inspect` and `docker stats`.

On your **Windows host PowerShell**, test VM port forwarding:

```powershell
Invoke-RestMethod "http://localhost:18000/health"
Start-Process "http://localhost:18000/docs"
```

Take screenshots of VM settings, Ubuntu terminal with `docker compose ps`, logs, inspect, stats, and the Windows request to port `18000`. These demonstrate the separate VM requirement.

## 5. What must be done manually

The VM creation, Docker installation, network forwarding, secret input and runtime screenshots are tasks on **your Windows machine**. The CI overlay does not execute them on your behalf.
