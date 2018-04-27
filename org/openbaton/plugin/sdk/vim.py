import logging
from abc import abstractmethod, ABCMeta

#
# Copyright (c) 2016 Open Baton (http://www.openbaton.org)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# package: org.openbaton.vim.drivers.interfaces
from org.openbaton.plugin.sdk.abstracts import AbstractVimDriver
from org.openbaton.plugin.sdk.catalogue import Server, NFVImage, Network, DeploymentFlavour, Subnet, Quota

log = logging.getLogger(__name__)


def is_vim_driver_subclass(clazz):
    return issubclass(clazz, VimDriver)


class VimDriver(AbstractVimDriver):
    __metaclass__ = ABCMeta

    @abstractmethod
    def launch_instance(self, vim_instance: dict,
                        name: str,
                        image: str,
                        flavor: str,
                        keypair: str,
                        networks: [dict],
                        security_groups: [str],
                        user_data: str) -> Server:
        """ generated source for method launchInstance """

    @abstractmethod
    def list_server(self, vim_instance: dict) -> [Server]:
        """ generated source for method listServer """

    @abstractmethod
    def rebuild_server(self, vim_instance: dict, server_id: str, image_id: str) -> Server:
        """ generated source for method rebuildServer """

    @abstractmethod
    def list_networks(self, vim_instance: dict) -> [Network]:
        """ generated source for method listNetworks """

    @abstractmethod
    def list_images(self, vim_instance: dict) -> [NFVImage]:
        """ generated source for method listImages """

    @abstractmethod
    def list_flavors(self, vim_instance: dict) -> [DeploymentFlavour]:
        """ generated source for method listFlavors """

    @abstractmethod
    def refresh(self, vim_instance: dict) -> dict:
        """ generated source for method refresh """

    @abstractmethod
    def launch_instance_and_wait(self,
                                 vim_instance: dict,
                                 instance_name: str,
                                 image: str,
                                 flavor: str,
                                 key_pair: str,
                                 networks: [dict],
                                 security_groups: [str],
                                 user_data: str,
                                 floating_ips: dict = None,
                                 keys: [dict] = None) -> Server:
        """ generated source for method launchInstanceAndWait """

    @abstractmethod
    def delete_server_by_id_and_wait(self, vim_instance: dict, ext_id: str):
        """ generated source for method deleteServerByIdAndWait """

    @abstractmethod
    def create_network(self, vim_instance: dict, network: dict) -> Network:
        """ generated source for method createNetwork """

    @abstractmethod
    def add_flavor(self, vim_instance: dict, deployment_flavour: dict) -> DeploymentFlavour:
        """ generated source for method addFlavor """

    @abstractmethod
    def add_image(self, vim_instance: dict, image: dict, image_file_or_url: str) -> NFVImage:
        """ generated source for method addImage """

    @abstractmethod
    def update_image(self, vim_instance: str, image: dict) -> NFVImage:
        """ generated source for method updateImage """

    @abstractmethod
    def copy_image(self, vim_instance: dict, image: dict, image_file: [bytes]) -> NFVImage:
        """ generated source for method copyImage """

    @abstractmethod
    def delete_image(self, vim_instance: dict, image: dict) -> bool:
        """ generated source for method deleteImage """

    @abstractmethod
    def update_flavor(self, vim_instance: dict, deployment_flavour: dict) -> DeploymentFlavour:
        """ generated source for method updateFlavor """

    @abstractmethod
    def delete_flavor(self, vim_instance: dict, ext_id: str) -> bool:
        """ generated source for method deleteFlavor """

    @abstractmethod
    def create_subnet(self, vim_instance: dict, created_network: dict, subnet: dict) -> Subnet:
        """ generated source for method createSubnet """

    @abstractmethod
    def update_network(self, vim_instance: dict, network: dict) -> Network:
        """ generated source for method updateNetwork """

    @abstractmethod
    def update_subnet(self, vim_instance: dict, updated_network: dict, subnet: dict) -> Subnet:
        """ generated source for method updateSubnet """

    @abstractmethod
    def get_subnets_ext_ids(self, vim_instance: dict, network_ext_id: str) -> [str]:
        """ generated source for method getSubnetsExtIds """

    @abstractmethod
    def delete_subnet(self, vim_instance: dict, existing_subnet_ext_id: str) -> bool:
        """ generated source for method deleteSubnet """

    @abstractmethod
    def delete_network(self, vim_instance: dict, ext_id: str) -> bool:
        """ generated source for method deleteNetwork """

    @abstractmethod
    def get_network_by_id(self, vim_instance: dict, ext_id: str) -> Network:
        """ generated source for method getNetworkById """

    @abstractmethod
    def get_quota(self, vim_instance: dict) -> Quota:
        """ generated source for method getQuota """

    @abstractmethod
    def get_type(self, vim_instance: dict) -> str:
        """ generated source for method getType """

