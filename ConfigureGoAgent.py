import getopt
import sys


def generateGoAgentDefaultFile(goServerUrl):
    f = open("go-agent", "w+")
    f.write('GO_SERVER_URL=' + goServerUrl + '\n')
    f.write('AGENT_WORK_DIR=/var/lib/${SERVICE_NAME:-go-agent}\n')
    f.close();

def generateAutoRegisterPropsFile(serverKey, regionCode, appCode, envCode):
    f = open("autoregister.properties", "w+")
    f.write('agent.auto.register.key=' + serverKey + '\n')
    f.write('agent.auto.register.resources=mw' + regionCode + '.agt.' + appCode + '.' + envCode + '\n')
    f.write('agent.auto.register.hostname=mw' + regionCode + '.host.' + appCode + '.' + envCode + '\n')
    f.close();

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "s:r:a:e:k:")
        serverUrl = ''
        serverKey = ''
        regionCode = ''
        appCode = ''
        envCode = ''
        for o,a in opts:
            if (o == '-s'):
                serverUrl = a;
            if (o == '-k'):
                serverKey = a;
            if (o == '-r'):
                regionCode = a;
            if (o == '-a'):
                appCode = a;
            if (o == '-e'):
                envCode = a;

        print('Generating default file ...')
        generateGoAgentDefaultFile(serverUrl);

        print('Generating auto register properties file ...')
        generateAutoRegisterPropsFile(serverKey, regionCode, appCode, envCode)
    except getopt.GetoptError as err:
        print(str(err))
        exit(2)

if __name__ == "__main__":
    main()
