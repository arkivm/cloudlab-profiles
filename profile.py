"""kernel static analysis"""

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg

# Create a portal context.
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

pc.defineParameter("DATASET", "URN of your image-backed dataset", 
                   portal.ParameterType.STRING,
                   "urn:publicid:IDN+emulab.net:xcap+ltdataset+vi")
pc.defineParameter("MOUNTPOINT", "Mountpoint for file system",
                   portal.ParameterType.STRING, "/local/device")

pc.defineParameter("DISKIMAGE", "Disk image",
                   portal.ParameterType.STRING,
                   "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU18-64-STD")
pc.defineParameter("HWTYPE", "Disk image",
                   portal.ParameterType.STRING,
                   "d820")


params = pc.bindParameters()

# Node node-0
node_0 = request.RawPC('node-0')
node_0.hardware_type = params.HWTYPE
node_0.disk_image = params.DISKIMAGE

iface = node_0.addInterface()

# Node blockhost-idisk
fsnode = request.RemoteBlockstore('fsnode', params.MOUNTPOINT)
fsnode.dataset = params.DATASET


# Now we add the link between the node and the special node
fslink = request.Link("fslink")
fslink.addInterface(iface)
fslink.addInterface(fsnode.interface)

# Special attributes for this link that we must use.
fslink.best_effort = True
fslink.vlan_tagging = True

# Install and execute a script that is contained in the repository.
#node.addService(pg.Execute(shell="sh", command="/local/repository/silly.sh"))

# Print the generated rspec
pc.printRequestRSpec(request)
