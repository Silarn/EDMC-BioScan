#!/bin/env python3

import urllib.parse
import urllib.request
import sys
import json
from RegionMapData import regions, regionmap

x0 = -49985
y0 = -40985
z0 = -24105


def findRegion(x, y, z):
    px = int((x - x0) * 83 / 4096)
    pz = int((z - z0) * 83 / 4096)

    if px < 0 or pz < 0 or pz >= len(regionmap):
        return None
    else:
        row = regionmap[pz]
        rx = 0

        for rl, pv in row:
            if px < rx + rl:
                break
            else:
                rx += rl
        else:
            pv = 0

        if pv == 0:
            return None
        else:
            return (pv, regions[pv])


def findRegionForBoxel(id64):
    masscode = id64 & 7
    z = (((id64 >> 3) & (0x3FFF >> masscode)) << masscode) * 10 + z0
    y = (((id64 >> (17 - masscode)) & (0x1FFF >> masscode)) << masscode) * 10 + y0
    x = (((id64 >> (30 - masscode * 2)) & (0x3FFF >> masscode)) << masscode) * 10 + x0

    return {
        'x': x,
        'y': y,
        'z': z,
        'region': findRegion(x, y, z)
    }


def findRegionsForSystems(sysname):
    url = 'https://www.edsm.net/api-v1/systems?systemName=' + urllib.parse.quote(sysname) + '&coords=1&showId=1'

    with urllib.request.urlopen(url) as f:
        systems = json.load(f)

    for system in systems:
        systemdata = {
            'name': system['name'],
            'id64': system['id64'] if 'id64' in system else None
        }

        if 'coords' in system:
            coords = system['coords']
            systemdata['x'] = x = coords['x']
            systemdata['y'] = y = coords['y']
            systemdata['z'] = z = coords['z']

            systemdata['region'] = findRegion(x, y, z)

        if 'id64' in system and system['id64']:
            systemdata['boxel'] = findRegionForBoxel(system['id64'])

        yield systemdata


def main():
    if len(sys.argv) <= 1:
        print('Usage: {0} "System Name" [...]'.format(sys.argv[0]))
        return

    for sysname in sys.argv[1:]:
        for sysdata in findRegionsForSystems(sysname):
            region = None

            if 'region' in sysdata:
                region = sysdata['region']
                if region is not None:
                    print('System {0} at ({1},{2},{3}) is in region {4} ({5})'.format(
                        sysdata['name'],
                        sysdata['x'],
                        sysdata['y'],
                        sysdata['z'],
                        region[0],
                        region[1]
                    ))
                else:
                    print('System {0} at ({1},{2},{3}) is outside the region map'.format(
                        sysdata['name'],
                        sysdata['x'],
                        sysdata['y'],
                        sysdata['z']
                    ))

            if 'boxel' in sysdata and sysdata['boxel']['region'] != region:
                region2 = sysdata['boxel']['region']

                if region2 is not None:
                    print('Boxel of system {0} at ({1},{2},{3}) is in region {4} ({5})'.format(
                        sysdata['name'],
                        sysdata['boxel']['x'],
                        sysdata['boxel']['y'],
                        sysdata['boxel']['z'],
                        region2[0],
                        region2[1]
                    ))
                else:
                    print('Boxel of system {0} at ({1},{2},{3}) is outside the region map'.format(
                        sysdata['name'],
                        sysdata['boxel']['x'],
                        sysdata['boxel']['y'],
                        sysdata['boxel']['z'],
                    ))


if __name__ == '__main__':
    main()