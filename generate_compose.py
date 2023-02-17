
import sys

try:
    try:
        n = int(sys.argv[1])
        if (n < 1 or n > 12):
            sys.exit("Error: number of drones must be between 1 and 12")
        print("Building compose for " + str(n) + " drones ...")
    except ValueError:
        sys.exit("Error: Please input an integer number of drones to simulate")

except IndexError:
    sys.exit("Error: Please input an integer number of dronese to simulate as first argument")

print("rest of the program")


# #Get the user to input a number of drones between 1 and 12
# badInput = True
# while(badInput == True):
#     print("How many drones in the swarm? (1-12): ")
#     drones = int(input())
#     if (drones > 0 and drones < 13):
#         badInput = False
#     else:
#         print("Bad input, please enter a number between 1 and 12")

# #Generate the env_files if asked
# #These files configure sitl
# for i in range(1,drones + 1):
#     filename = "./env_files/env" + str(i)
#     f = open(filename,"w")
#     instance =  "INSTANCE=0\n"
#     lat =       "LAT=40.846\n"
#     lon =       "LON=-96.47" + str(i) + "\n"
#     alt =       "ALT=390\n"
#     dir =       "DIR=0\n"
#     model =     "MODEL=+\n"
#     vehicle =   "VEHICLE=ArduCopter\n"
#     f.writelines([instance,lat,lon,alt,dir,model,vehicle])
#     f.close()

# #Generate the ros_envs
# #These files configure the clustering control
# for i in range(1,drones + 1):
#     filename = "./env_files/ros_env" + str(i)
#     f = open(filename,"w")
#     port =              "PORT=tcp://0.0.0.0:5760\n"             #Same across all vehicles
#     sysId =             "SYS_ID=" + str(i) + "\n"               #Different for each vehicle
#     compId =            "COMP_ID=2\n"                           #Same across all vehicles
#     clusterId =         "CLUSTER_ID=1\n"                        #Same across all vehicles
#     clusterPos =        "CLUSTER_POSITION=" + str(i) + "\n"     #Different for each vehicle
#     clusterSize =       "CLUSTER_SIZE=" + str(drones + 1) + "\n"                        
#     clusterRad =        "CLUSTER_RADIUS=16\n"
#     agentAlt =          "AGENT_ALT=" + str(i * 3.0) + "\n"
#     homeLat =           "HOME_LAT=40.8467784\n"
#     homeLon =           "HOME_LON=-96.4719180\n"
#     homeAlt =           "HOME_ALT=400\n"
#     rally1Lat =         "RALLY1LAT=0\n"
#     rally1Lon =         "RALLY1LON=30\n"
#     rally2Lat =         "RALLY2LAT=30\n"
#     rally2Lon =         "RALLY2LON=0\n"
#     f.writelines([port,sysId,compId,clusterId,clusterPos,clusterSize,clusterRad,agentAlt,homeLat,homeLon,homeAlt,rally1Lat,rally1Lon,rally2Lat,rally2Lon])
#     f.close()

# #Generate the mavlink router file
# mavlinkConfig = "./mavlink_router/main.conf"
# f = open(mavlinkConfig,"w")
# for i in range(1,drones + 1):
#     name =      "[TcpEndpoint sitl_" + str(i) + "]\n"
#     address =   "Address = 0.0.0.0\n"
#     port =      "Port = 4" + str(i) + "02\n\n"
#     f.writelines([name,address,port])

# #Add the main UPD connection
# name =      "[UdpEndpoint omega]\n"
# mode =      "Mode=Normal\n"
# address =   "Address = 0.0.0.0\n"
# port =      "Port = 4242\n"
# f.writelines([name,mode,address,port])
# f.close()


# #"global" variables
# debugContainerPort = "5760"
# networkContainerPort = "5762"
# mavrosContainerPort = "5763"


# #Initialize port lists
# debugHostPort = ["blank"]
# networkHostPort = ["blank"]
# mavrosHostPort = ["blank"]

# #Create a docker-compose file Header
# f = open("./docker-compose.yaml","w")
# f.writelines(["version: '3'\n\n","services:\n"])

# #SITL Images:
# for i in range(1,drones+1):
#     var = str(i)

#     container =         "  sitl_" + var + ":\n"
#     image =             "    image: ghcr.io/grantphllps/ardupilot_docker:latest\n"
#     containerName =     "    container_name: sitl" + var + "\n"
#     ports =             "    ports:\n"
#     debugPort =         '      - "4' + var + '00:5760"\n'
#     netwoPort =         '      - "4' + var + '02:5762"\n'
#     mavroPort =         '      - "4' + var + '03:5763"\n'
#     volumes =           '    volumes:\n'
#     envVol =            '      - ./env_files:/root/home/env_files\n'
#     command =           '    command: >\n'
#     comman1 =           '      /bin/bash -c "export $$(cat /root/home/env_files/env' + var + ') &&\n'
#     comman2 =           '                    /home/ardupilot/Tools/autotest/sim_vehicle.py --vehicle $${VEHICLE} -w --custom-location=$${LAT},$${LON},$${ALT},$${DIR}  --no-rebuild --add-param-file=/home/ardupilot/Tools/autotest/default_params/gazebo-drone' + var + '.parm"\n'
    
#     f.writelines([container,image,containerName,ports,debugPort,netwoPort,mavroPort,volumes,envVol,command,comman1,comman2,"\n"])

#     container =         "  clustering_" + var + ":\n"
#     depends =           "    depends_on:\n"
#     depend1 =           "      - sitl_" + var + "\n"
#     image =             "    image: ghcr.io/grantphllps/clustering:latest\n"
#     containerName =     "    container_name: clustering_" + var + "\n"
#     options1 =          "    stdin_open: true\n"
#     options2 =          "    tty: true\n"
#     volumes =           '    volumes:\n'
#     envVol =            '      - ./env_files:/root/home/env_files\n'
#     link =              '    links:\n'
#     link1 =             '      - sitl_' + var + '\n'
#     command =           '    command: >\n'
#     comman1 =           '      /bin/bash -c "source /home/catkin_ws/devel/setup.bash &&\n'
#     comman2 =           '                    export $$(cat /root/home/env_files/ros_env' + var +')\n'
#     comman3 =           '                    roslaunch src/clustering_control/launch/clustering_control_container.launch system_ID:=$${SYS_ID} clusterID:=$${CLUSTER_ID} clusterPosition:=$${CLUSTER_POSITION} clusterSize:=$${CLUSTER_SIZE} clusterRadius:=$${CLUSTER_RADIUS} agentAlt:=$${AGENT_ALT} homeLat:=$${HOME_LAT} homeLon:=$${HOME_LON} homeAlt:=$${HOME_ALT} rally1Lat:=$${RALLY1LAT} rally1Lon:=$${RALLY1LON} rally2Lat:=$${RALLY2LAT} rally2Lon:=$${RALLY2LON} fcu_url:=tcp://sitl' + var + ':5763 tgt_system:=$${SYS_ID} tgt_component:=$${COMP_ID}"\n'

#     f.writelines([container,depends,depend1,image,containerName,options1,options2,volumes,envVol,link,link1,command,comman1,comman2,comman3,"\n"])

# #Mavlink router
# container =         "  mavlink_router:\n"
# image =             "    image: ghcr.io/grantphllps/mavlink_router:latest\n"
# containerName =     "    container_name: mavlink_router\n"
# depends =           "    depends_on:\n"
# f.writelines([container,image,containerName,depends])
# #Mavlink router depends
# for i in range(1,drones+1):
#     var = str(i)    
#     depend =           "      - sitl_" + var + "\n"
#     f.write(depend)
# options1 =          "    stdin_open: true\n"
# options2 =          "    tty: true\n"
# network =           '    network_mode: "host"\n'
# volume =            '    volumes:\n'
# volume1 =           '      - ./mavlink_router:/root/home/mavlink_router_files\n'
# command =           '    command: >\n'
# command1 =          '      /bin/bash -c "mavlink-routerd -c /root/home/mavlink_router_files/main.conf"'


# f.writelines([options1,options2,network,volume,volume1,command,command1])
# f.close()