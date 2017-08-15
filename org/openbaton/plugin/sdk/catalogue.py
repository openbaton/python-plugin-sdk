#!/usr/bin/env python
""" generated source for module NFVImage """

#
#  * Copyright (c) 2016 Open Baton (http://www.openbaton.org)
#  *
#  * Licensed under the Apache License, Version 2.0 (the "License");
#  * you may not use this file except in compliance with the License.
#  * You may obtain a copy of the License at
#  *
#  *      http://www.apache.org/licenses/LICENSE-2.0
#  *
#  * Unless required by applicable law or agreed to in writing, software
#  * distributed under the License is distributed on an "AS IS" BASIS,
#  * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  * See the License for the specific language governing permissions and
#  * limitations under the License.
#  *
#  
# package: org.openbaton.catalogue.nfvo
from datetime import date


class _BaseObject(object):
    def get_dict(self):
        return self.__dict__


class ImageStatus:
    """ generated source for enum ImageStatus """
    UNRECOGNIZED = u'UNRECOGNIZED'
    ACTIVE = u'ACTIVE'
    SAVING = u'SAVING'
    QUEUED = u'QUEUED'
    KILLED = u'KILLED'
    PENDING_DELETE = u'PENDING_DELETE'
    DELETED = u'DELETED'


class NFVImage(_BaseObject):
    def __init__(self, _id: str = None,
                 version: str = None,
                 ext_id: str = None,
                 name: str = None,
                 min_ram: int = None,
                 min_disk_space: int = None,
                 min_cpu: str = None,
                 is_public: bool = False,
                 disk_format: str = None,
                 container_format: str = None,
                 created: date = None,
                 updated: date = None,
                 status: ImageStatus = None):
        self.id = _id
        self.version = version
        self.extId = ext_id
        self.name = name
        self.minRam = min_ram

        self.minDiskSpace = min_disk_space

        self.minCPU = min_cpu
        self.isPublic = is_public
        self.diskFormat = disk_format
        self.containerFormat = container_format
        self.created = created
        self.updated = updated
        self.status = status

    def __str__(self):
        """ generated source for method toString """
        if self.created:
            created_isoformat = self.created.isoformat()
        else:
            created_isoformat = "None"
        if self.updated:
            updated_isoformat = self.updated.isoformat()
        else:
            updated_isoformat = "None"
        return "Image{" + \
               "id='" + self.id + '\'' + \
               ", name='" + self.name + '\'' + \
               ", version=" + self.version + \
               ", extId='" + self.extId + '\'' + \
               ", minRam='" + str(self.minRam) + '\'' + \
               ", minDiskSpace='" + str(self.minDiskSpace) + '\'' + \
               ", minCPU='" + self.minCPU + '\'' + \
               ", public='" + str(self.isPublic) + '\'' + \
               ", diskFormat='" + self.diskFormat + '\'' + \
               ", containerFormat='" + self.containerFormat + '\'' + \
               ", status='" + str(self.status) + '\'' + \
               ", created='" + created_isoformat + '\'' + \
               ", updated='" + updated_isoformat + '\'' + '}'


class Subnet(_BaseObject):
    """ generated source for class Subnet """

    def __init__(self, _id: str = None, _version: int = None, name: str = None, ext_id: str = None,
                 network_id: str = None, cidr: str = None, gateway_ip: str = None):
        self.id = _id
        self.version = _version
        self.name = name
        self.extId = ext_id
        self.networkId = network_id
        self.cidr = cidr
        self.gatewayIp = gateway_ip

    def __str__(self):
        """ generated source for method toString """
        return "Subnet{" + "id='" + self.id + '\'' + ", version=" + str(self.version) + \
               ", name='" + self.name + '\'' + ", extId='" + self.extId + '\'' + \
               ", networkId='" + self.networkId + '\'' + ", cidr='" + self.cidr + '\'' + \
               ", gatewayIp='" + self.gatewayIp + '\'' + '}'


class Network(_BaseObject):
    def __init__(self, _id: str = None, version: int = None, name: str = None, ext_id: str = None,
                 external: bool = False, shared: bool = False, subnets: [Subnet] = []):
        self.id = _id
        self.version = version
        self.name = name
        self.extId = ext_id
        self.external = external
        self.shared = shared
        self.subnets = subnets

    def __str__(self):
        """ generated source for method toString """
        return "Network{" + "id='" + self.id + '\'' + ", name='" + self.name + '\'' + \
               ", extId='" + self.extId + '\'' + ", external=" + str(self.external) + \
               ", shared=" + str(self.shared) + ", subnets=" + str(self.subnets) + '}'

    def get_dict(self):
        _dict = self.__dict__
        if self.subnets:
            _dict['subnets'] = [sub.__dict__ for sub in self.subnets]
        else:
            _dict.pop('subnets', None)
        return _dict


class DeploymentFlavour(_BaseObject):
    """ generated source for class DeploymentFlavour """

    def __init__(self, _id: str = None, _version: int = None, flavour_key: str = None, ext_id: str = None,
                 ram: int = None,
                 disk: int = None, vcpu: int = None):
        # ID of the deployment flavour.
        self.id = _id
        self.version = _version
        #
        # Assurance parameter against which this flavour is being described. The key could be a combination of
        # multiple assurance parameters with a logical relationship between them. The parameters should be present as
        #  a monitoring_parameter supported in clause 6.2.1.1. For example, a flavour of a virtual EPC could be
        # described in terms of the assurance parameter "calls per second" (cps).
        #
        self.flavour_key = flavour_key
        self.extId = ext_id
        self.ram = ram
        self.disk = disk
        self.vcpus = vcpu

    def __str__(self):
        """ generated source for method toString """
        return "DeploymentFlavour{" + "id='" + self.id + '\'' + ", version=" + str(self.version) + \
               ", flavour_key='" + self.flavour_key + '\'' + ", extId='" + self.extId + '\'' + '}'


class Location(_BaseObject):
    """ generated source for class Location """

    def __init__(self, _id=None, _version=None, name=None, latitude=None, longitude=None):
        self.id = _id
        self.version = _version
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        """ generated source for method toString """
        return "Location{" + "id='" + self.id + '\'' + ", version=" + self.version + ", name='" + self.name + '\'' + ", latitude='" + self.latitude + '\'' + ", longitude='" + self.longitude + '\'' + '}'


class VimInstance(_BaseObject):
    """ generated source for class VimInstance """

    def __init__(self, _id: str = None, _version: int = None, name: str = None, auth_url: str = None,
                 tenant: str = None, username: str = None, password: str = None,
                 key_pair: str = None, location: Location = None, security_groups: list = None, flavours: list = None,
                 _type: str = None, images: list = None,
                 networks: list = None, project_id: str = None, active: bool = None):
        self.id = _id
        self.version = _version
        self.name = name
        self.authUrl = auth_url
        self.tenant = tenant
        self.username = username
        self.password = password
        self.keyPair = key_pair
        self.location = location
        self.securityGroups = security_groups
        self.flavours = flavours
        self.type = _type
        self.images = images
        self.networks = networks
        self.projectId = project_id
        self.active = active

    def __str__(self):
        """ generated source for method toString """
        return "VimInstance{" + "id='" + self.id + '\'' + ", version=" + str(
            self.version) + ", name='" + self.name + '\'' + ", authUrl='" + self.authUrl + '\'' + ", tenant='" + self.tenant + '\'' + ", username='" + self.username + '\'' + ", password='************'" + ", keyPair='" + self.keyPair + '\'' + ", location=" + str(
            self.location) + ", securityGroups=" + str(
            self.securityGroups) + ", flavours=" + str(
            self.flavours) + ", type='" + self.type + '\'' + ", images=" + str(self.images) + ", networks=" + str(
            self.networks) + ", projectId='" + self.projectId + '\'' + ", active=" + str(self.active) + '}'

    def get_dict(self):
        _dict = self.__dict__
        if self.location:
            _dict['location'] = self.location.__dict__
        else:
            _dict.pop('location', None)
        return _dict


class Server(_BaseObject):
    """ generated source for class Server """

    def __init__(self, _id: str = None,
                 _version: int = None,
                 name: str = None,
                 image: NFVImage = None,
                 flavor: DeploymentFlavour = None,
                 status: str = None,
                 extended_status: str = None,
                 ext_id: str = None,
                 ips: dict = None,
                 floating_ips: dict = None,
                 created: date = None,
                 updated: date = None,
                 hostname: str = None,
                 hypervisor_host_name: str = None,
                 instance_name: str = None):
        self.id = _id
        self.version = _version
        self.name = name
        self.image = image
        self.flavor = flavor
        self.status = status
        self.extendedStatus = extended_status
        self.extId = ext_id
        self.ips = ips  # dict
        self.floatingIps = floating_ips
        self.created = created
        self.updated = updated
        self.hostName = hostname
        self.hypervisorHostName = hypervisor_host_name
        self.instanceName = instance_name

    def __str__(self):
        """ generated source for method toString """
        return "Server{" + "id='" + self.id + '\'' + ", version=" + str(
            self.version) + ", name='" + self.name + '\'' + ", image=" + str(self.image) + ", flavor=" + str(
            self.flavor) + ", status='" + self.status + '\'' + ", extendedStatus='" + self.extendedStatus + '\'' + ", extId='" + self.extId + '\'' + ", ips=" + str(
            self.ips) + ", floatingIps=" + str(self.floatingIps) + ", created=" + str(
            self.created) + ", updated=" + str(
            self.updated) + ", hostName='" + self.hostName + '\'' + ", hypervisorHostName='" + self.hypervisorHostName + '\'' + ", instanceName='" + self.instanceName + '\'' + '}'

    def get_dict(self):
        _dict = self.__dict__
        if self.image:
            _dict['image'] = self.image.__dict__
        else:
            _dict.pop('image', None)
        if self.flavor:
            _dict['flavor'] = self.flavor.__dict__
        else:
            _dict.pop('flavor', None)
        return _dict


class Quota(_BaseObject):
    """ generated source for class Quota """

    def __init__(self, _id: str = None, _version: int = None, tenant: str = None, cores: int = None,
                 floating_ips: int = None,
                 instances: int = None, keypairs: int = None, ram: int = None):
        self.id = _id
        self.version = _version
        self.tenant = tenant
        self.cores = cores
        self.floatingIps = floating_ips
        self.instances = instances
        self.keyPairs = keypairs
        self.ram = ram

    def __str__(self):
        """ generated source for method toString """
        return "Quota{" + "id='" + self.id + '\'' + ", version=" + self.version + ", tenant='" + self.tenant + '\'' + ", cores='" + self.cores + '\'' + ", floatingIps='" + self.floatingIps + '\'' + ", instances='" + self.instances + '\'' + ", keypairs='" + self.keyPairs + '\'' + ", ram='" + self.ram + '\'' + '}'
