import subprocess, re, random, time

def checkVPN():
    status = subprocess.Popen(['nordvpn','status'], stdout=subprocess.PIPE).stdout.read()
    status = re.split(r'[\r\n]', status.decode("utf-8"))
    status = [i for i in status if i.strip() not in ['','-']]
    statusDict = {}
    for i in status:
        k = i.split(':')[0].strip()
        v = i.split(':')[1].strip()
        statusDict[k] = v
    
    return statusDict

def getContries():
    countries = subprocess.Popen(['nordvpn','countries'], stdout=subprocess.PIPE).stdout.read()
    countries = re.split(r'[\r\t\n]',countries.decode("utf-8"))
    countries = [i for i in countries if i.strip() not in ['','-']]
    return countries


def connectVPN(country):
    out = subprocess.call(['nordvpn','connect',country])


def randomizeNord():
    timeOfChanges = int(input('Time in seconds between VPN changes: '))
    subprocess.call(['nordvpn','connect'])
    while True:
        time.sleep(timeOfChanges)

        status = checkVPN()
        for k,v in status.items():
            print(f'{k}: {v}')
        
        countries = getContries()
        countryRandom = random.choice(countries)

        print(f"Previously connected to {status['Country']}")
        print(f'Switching to {countryRandom}')
        connectVPN(countryRandom)

if __name__ == '__main__':
    randomizeNord()
