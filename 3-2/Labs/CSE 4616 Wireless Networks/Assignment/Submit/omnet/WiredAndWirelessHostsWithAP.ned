import inet.node.ethernet.Eth100M;
import inet.node.inet.AccessPoint;
import inet.node.inet.Router;
import inet.node.inet.StandardHost;
import inet.node.wireless.WirelessHost;
import inet.physicallayer.wireless.common.contract.packetlevel.IRadioMedium;

network WiredAndWirelessHostsWithAP
{
    parameters:
        int numWirelessHosts = default(2);
        int numWiredHosts = default(0);

        @display("bgb=700,500");

    submodules:
        radioMedium: <default("RadioMedium")> like IRadioMedium {
            @display("p=80,70");
        }

        ap: AccessPoint {
            @display("p=300,250");
        }

        router: Router {
            @display("p=450,250");
        }

        wiredSinkNode: StandardHost {
            @display("p=600,250");
        }

        wirelessHost[numWirelessHosts]: WirelessHost {
            @display("p=120,100");
        }

        wiredHost[numWiredHosts]: StandardHost {
            @display("p=450,120");
        }

    connections:
        for i = 0..numWiredHosts-1 {
            wiredHost[i].ethg++ <--> Eth100M <--> router.ethg++;
        }

        router.ethg++ <--> Eth100M <--> ap.ethg++;

        router.ethg++ <--> Eth100M <--> wiredSinkNode.ethg++;
}