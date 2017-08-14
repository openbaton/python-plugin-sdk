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
from org.openbaton.plugin.sdk.abstracts import AbstractPluginHelper

log = logging.getLogger("org.openbaton.plguin.vim.sdk.%s" % __name__)


def is_vim_driver_subclass(clazz):
    return issubclass(clazz, VimDriver)


class VimDriver(AbstractPluginHelper):
    __metaclass__ = ABCMeta

    @abstractmethod
    def launch_instance(self, vim_instance, name, image, flavor, keypair, networks, security_groups, user_data):
        """ generated source for method launchInstance """

    @abstractmethod
    def list_images(self, vim_instance):
        """ generated source for method listImages """

    @abstractmethod
    def list_server(self, vim_instance):
        """ generated source for method listServer """

    @abstractmethod
    def list_networks(self, vim_instance):
        """ generated source for method listNetworks """

    @abstractmethod
    def list_flavors(self, vim_instance):
        """ generated source for method listFlavors """

    @abstractmethod
    def launch_instance_and_wait(self,
                                 vim_instance,
                                 hostname,
                                 image,
                                 ext_id,
                                 key_pair,
                                 networks,
                                 security_groups,
                                 user_data,
                                 floating_ips=None,
                                 keys=None):
        """ generated source for method launchInstanceAndWait """

    @abstractmethod
    def delete_server_by_id_and_wait(self, vim_instance, ext_id):
        """ generated source for method deleteServerByIdAndWait """

    @abstractmethod
    def create_network(self, vim_instance, network):
        """ generated source for method createNetwork """

    @abstractmethod
    def add_flavor(self, vim_instance, deployment_flavour):
        """ generated source for method addFlavor """

    @abstractmethod
    def add_image(self, vim_instance, image, image_file_or_url):
        """ generated source for method addImage """

    @abstractmethod
    def update_image(self, vim_instance, image):
        """ generated source for method updateImage """

    @abstractmethod
    def copy_image(self, vim_instance, image, image_file):
        """ generated source for method copyImage """

    @abstractmethod
    def delete_image(self, vim_instance, image):
        """ generated source for method deleteImage """

    @abstractmethod
    def update_flavor(self, vim_instance, deployment_flavour):
        """ generated source for method updateFlavor """

    @abstractmethod
    def delete_flavor(self, vim_instance, ext_id):
        """ generated source for method deleteFlavor """

    @abstractmethod
    def create_subnet(self, vim_instance, created_network, subnet):
        """ generated source for method createSubnet """

    @abstractmethod
    def update_network(self, vim_instance, network):
        """ generated source for method updateNetwork """

    @abstractmethod
    def update_subnet(self, vim_instance, updated_network, subnet):
        """ generated source for method updateSubnet """

    @abstractmethod
    def get_subnets_ext_ids(self, vim_instance, network_ext_id):
        """ generated source for method getSubnetsExtIds """

    @abstractmethod
    def delete_subnet(self, vim_instance, existing_subnet_ext_id):
        """ generated source for method deleteSubnet """

    @abstractmethod
    def delete_network(self, vim_instance, ext_id):
        """ generated source for method deleteNetwork """

    @abstractmethod
    def get_network_by_id(self, vim_instance, ext_id):
        """ generated source for method getNetworkById """

    @abstractmethod
    def get_quota(self, vim_instance):
        """ generated source for method getQuota """

    @abstractmethod
    def get_type(self, vim_instance):
        """ generated source for method getType """
