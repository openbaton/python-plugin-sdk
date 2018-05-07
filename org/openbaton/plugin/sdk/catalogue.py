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
from enum import Enum


class _BaseObject(object):
    def get_dict(self):
        return dict(self.__dict__)


class ImageStatus(Enum):
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
                 created: str = None,
                 updated: str = None,
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
        return "Image{" + \
               "id='" + str(self.id) + '\'' + \
               ", name='" + str(self.name) + '\'' + \
               ", version=" + str(self.version) + \
               ", extId='" + str(self.extId) + '\'' + \
               ", minRam='" + str(self.minRam) + '\'' + \
               ", minDiskSpace='" + str(self.minDiskSpace) + '\'' + \
               ", minCPU='" + str(self.minCPU) + '\'' + \
               ", public='" + str(self.isPublic) + '\'' + \
               ", diskFormat='" + str(self.diskFormat) + '\'' + \
               ", containerFormat='" + str(self.containerFormat) + '\'' + \
               ", status='" + str(self.status.value) + '\'' if self.status else 'None' + '\'' + \
               ", created='" + str(self.created) + '\'' + \
               ", updated='" + str(self.updated) + '\'' + '}'

    def get_dict(self):
        _dict = dict(self.__dict__)
        if self.status is not None and self.status.value is not None:
            _dict['status'] = self.status.value
        else:
            _dict.pop('status', None)
        return _dict


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
        return "Subnet{" + "id='" + str(self.id) + '\'' + ", version=" + str(self.version) + \
               ", name='" + str(self.name) + '\'' + ", extId='" + str(self.extId) + '\'' + \
               ", networkId='" + str(self.networkId) + '\'' + ", cidr='" + str(self.cidr) + '\'' + \
               ", gatewayIp='" + str(self.gatewayIp) + '\'' + '}'


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
        return "Network{" + "id='" + str(self.id) + '\'' + ", name='" + str(self.name) + '\'' + \
               ", extId='" + str(self.extId) + '\'' + ", external=" + str(self.external) + \
               ", shared=" + str(self.shared) + ", subnets=" + str([str(sn) for sn in self.subnets if self.subnets]) + '}'

    def get_dict(self):
        _dict = dict(self.__dict__)
        if self.subnets is not None:
            _dict['subnets'] = [sub.get_dict() for sub in self.subnets]
        else:
            _dict.pop('subnets', None)
        return _dict


class DeploymentFlavour(_BaseObject):
    """ generated source for class DeploymentFlavour """

    def __init__(self, _id: str = None, _version: int = None, flavour_key: str = None, ext_id: str = None,
                 ram: int = None, disk: int = None, vcpu: int = None):
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
        return "DeploymentFlavour{" + "id='" + str(self.id) + '\'' + ", version=" + str(self.version) + \
               ", flavour_key='" + str(self.flavour_key) + '\'' + ", extId='" + str(self.extId) + '\'' + '}'


class Location(_BaseObject):
    """ generated source for class Location """

    def __init__(self, _id: str = None, _version: int = None, name: str = None, latitude: str = None,
                 longitude: str = None):
        self.id = _id
        self.version = _version
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        """ generated source for method toString """
        return "Location{" + "id='" + str(self.id) + '\'' + ", version=" + str(self.version) + \
               ", name='" + str(self.name) + '\'' + ", latitude='" + str(self.latitude) + '\'' + \
               ", longitude='" + str(self.longitude) + '\'' + '}'

class AvailabilityZone(_BaseObject):
    def __init__(self, _id: str = None, _version: int = None, name: str = None, available: bool = None, hosts: dict = {}):
        self.id = _id
        self.version = _version
        self.name = name
        self.available = available
        self.hosts = hosts

    def __str__(self):
        return "AvailabilityZone{" + "id='" + str(self.id) + '\'' + ", version=" + str(self.version) + \
               ", name='" + str(self.name) + '\'' + ", available=" + str(self.available) + \
               ", hosts=" + str(self.hosts) + '}'

class PopKeypair(_BaseObject):
    def __init__(self, _id: str = None, _version: int = None, name: str = None, public_key: str = None, fingerprint: str = None):
        self.id = _id
        self.version = _version
        self.name = name
        self.publicKey = public_key
        self.fingerprint = fingerprint

    def __str__(self):
        return "AvailabilityZone{" + "id='" + str(self.id) + '\'' + ", version=" + str(self.version) + \
               ", name='" + str(self.name) + '\'' + ", publicKey='" + str(self.publicKey) + \
               "', fingerprint='" + str(self.fingerprint) + '\'}'



class BaseVimInstance(_BaseObject):
    """ generated source for class VimInstance """

    def __init__(self, _id: str = None, _version: int = None, name: str = None, auth_url: str = None,
                 tenant: str = None, username: str = None, password: str = None,
                 key_pair: str = None, location: Location = None, security_groups: list = None, flavours: [DeploymentFlavour] = None,
                 _type: str = None, images: list = None,
                 networks: [Network] = None, project_id: str = None, active: bool = None):
        self.id = _id
        self.version = _version
        self.name = name
        self.authUrl = auth_url
        self.location = location
        self.type = _type
        self.images = images
        self.networks = networks
        self.active = active

    def __str__(self):
        """ generated source for method toString """
        return "VimInstance{" + "id='" + str(self.id) + '\'' + ", version=" + str(
            self.version) + ", name='" + str(self.name) + '\'' + ", authUrl='" + str(self.authUrl) + '\'' + \
            ", location=" + str(self.location) + ", type='" + str(self.type) + '\'' + \
            ", images=" + str(self.images) + ", networks=" + str([str(n) for n in self.networks if self.networks]) + \
            ", active=" + str(self.active) + '}'

    def get_dict(self):
        _dict = dict(self.__dict__)
        if self.location is not None:
            _dict['location'] = self.location.get_dict()
        else:
            _dict.pop('location', None)
        if self.images is not None:
            _dict['images'] = [image.get_dict() for image in self.images]
        else:
            _dict.pop('images', None)
        if self.networks is not None:
            _dict['networks'] = [net.get_dict() for net in self.networks]
        else:
            _dict.pop('networks', None)
        return _dict

class OpenstackVimInstance(BaseVimInstance):
    def __init__(self, _id: str = None, _version: int = None, name: str = None, auth_url: str = None,
                 tenant: str = None, username: str = None, password: str = None,
                 key_pair: str = None, location: Location = None, security_groups: list = None, flavours: [DeploymentFlavour] = [],
                 _type: str = None, images: list = None, networks: [Network] = [], zones: [AvailabilityZone] = [],
                 project_id: str = None, active: bool = None):
        super(OpenstackVimInstance, self).__init__(_id=_id, _version=_version, name=name, auth_url=auth_url, images=images,
                                                   networks=networks, location=location, type=_type, active=active)

        self.tenant = tenant
        self.username = username
        self.password = password
        self.keyPair = key_pair
        self.securityGroups = security_groups
        self.flavours = flavours
        self.projectId = project_id
        self.zones = zones

    def __str__(self):
        """ generated source for method toString """
        return "VimInstance{" + "id='" + str(self.id) + '\'' + ", version=" + str(
            self.version) + ", name='" + str(self.name) + '\'' + ", authUrl='" + str(self.authUrl) + '\'' + \
            ", tenant='" + str(self.tenant) + '\'' + ", username='" + str(self.username) + '\'' + \
            ", password='************'" + ", keyPair='" + str(self.keyPair) + '\'' + ", location=" + str(
            self.location) + ", securityGroups=" + str(self.securityGroups) + ", flavours=" + str(
            [str(f) for f in self.flavours if self.flavours]) + ", zones=" + str([str(z) for z in self.zones if self.zones]) + \
            ", type='" + str(self.type) + '\'' + ", images=" + str(self.images) + ", networks=" + \
            str([str(n) for n in self.networks if self.networks]) + ", projectId='" + str(self.projectId) + '\'' + \
            ", active=" + str(self.active) + '}'

    def get_dict(self):
        _super_dict = super(BaseVimInstance, self).get_dict()
        _dict = dict(self.__dict__)
        if self.flavours is not None:
            _dict['flavours'] = [flavour.get_dict() for flavour in self.flavours]
        else:
            _dict.pop('flavours', None)
        for key in _super_dict:
            value = _dict.get(key)
            # if the value is not a primitive type or a list of primitive types overwrite the value in _dict with the value from _super_dict
            if value is None or (type(value) in (dict, str, int, bool) or
                 (type(value) == list and (len(value)==0 or type(value[0]) in (dict, str, int, bool)))):
                continue
            _dict[key] = _super_dict.get(key)
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
                 created: str = None,
                 updated: str = None,
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
        return "Server{" + "id='" + str(self.id) + '\'' + ", version=" + str(
            self.version) + ", name='" + str(self.name) + '\'' + ", image=" + str(self.image) + ", flavor=" + str(
            self.flavor) + ", status='" + str(self.status) + '\'' + ", extendedStatus='" + str(self.extendedStatus) + \
            '\'' + ", extId='" + str(self.extId) + '\'' + ", ips=" + str(self.ips) + ", floatingIps=" + str(self.floatingIps) + \
            ", created=" + str(self.created) + ", updated=" + str(self.updated) + ", hostName='" + str(self.hostName) + '\'' + \
            ", hypervisorHostName='" + str(self.hypervisorHostName) + '\'' + ", instanceName='" + str(self.instanceName) + '\'' + '}'

    def get_dict(self):
        _dict = dict(self.__dict__)
        if self.image:
            _dict['image'] = self.image.get_dict()
        else:
            _dict.pop('image', None)
        if self.flavor:
            _dict['flavor'] = self.flavor.get_dict()
        else:
            _dict.pop('flavor', None)
        return _dict


class Quota(_BaseObject):
    """ generated source for class Quota """

    def __init__(self, _id: str = None, _version: int = None, tenant: str = None, cores: int = None,
                 floating_ips: int = None, instances: int = None, keypairs: int = None, ram: int = None):
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
        return "Quota{" + "id='" + str(self.id) + '\'' + ", version=" + str(self.version) + ", tenant='" + \
               str(self.tenant) + '\'' + ", cores='" + str(self.cores) + '\'' + ", floatingIps='" + \
               str(self.floatingIps) + '\'' + ", instances='" + str(self.instances) + '\'' + ", keypairs='" + \
               str(self.keyPairs) + '\'' + ", ram='" + str(self.ram) + '\'' + '}'

