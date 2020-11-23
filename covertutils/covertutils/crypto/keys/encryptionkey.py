from abc import ABCMeta, abstractmethod


class EncryptionKey(metaclass=ABCMeta) :

	@abstractmethod
	def encrypt( self, plain ) : pass
	@abstractmethod
	def decrypt( self, crypt ) : pass
