from string import ascii_letters

from covertutils.crypto.keys import StandardCyclingKey
from covertutils.crypto.algorithms import StandardCyclingAlgorithm

from covertutils.helpers import sxor, xor_str

from covertutils.exceptions import *


class StreamIdentifier :

	__comparer = ascii_letters

	def __init__( self, passphrase, stream_list = [], cycling_algorithm = None, reverse = False, hard_stream = 'control' ) :

		self.cycle = True		# For testing
		# self.cycle = False		# For testing
		if cycling_algorithm == "No" :
			self.cycle = False

		self.cycling_algorithm = cycling_algorithm
		if self.cycling_algorithm == None :
			self.cycling_algorithm = StandardCyclingAlgorithm

		self.__streams = {}
		self.hashphrase = self.cycling_algorithm( passphrase ).digest()

		stream_list = set( stream_list )
		self.__hard_stream = hard_stream
		stream_list.add( self.__hard_stream )	# be sure that the list contains a control stream
		# self.__stream_generator = StandardCyclingKey( passphrase, cycling_algorithm )

		self.reverse = reverse
		for stream_name in stream_list :
			self.addStream( stream_name )


	def addStream( self, stream_name ) :
		if stream_name in list(self.__streams.keys()) :
			raise StreamAlreadyExistsException( "Stream '%s' already exists" % stream_name )

		inp_passphrase = self.cycling_algorithm( self.hashphrase + stream_name ).digest()
		#print("In addStream of streamIndentifier, the inp_passphrase is: %s" % inp_passphrase)
		out_passphrase = self.cycling_algorithm( stream_name + self.hashphrase ).digest()
		#print("In addStream of streamIndentifier, the out_passphrase is: %s" % out_passphrase)
		if self.reverse :
			inp_passphrase, out_passphrase = out_passphrase, inp_passphrase

		not_hard_stream = self.__hard_stream != stream_name
		inp_StandardCyclingKey = StandardCyclingKey ( inp_passphrase, cycling_algorithm = self.cycling_algorithm, cycle_enabled = not_hard_stream )
		out_StandardCyclingKey = StandardCyclingKey ( out_passphrase, cycling_algorithm = self.cycling_algorithm, cycle_enabled = not_hard_stream )

		StandardCyclingKey_tuple = ( inp_StandardCyclingKey, out_StandardCyclingKey )
		self.__streams[stream_name] = StandardCyclingKey_tuple


	def deleteStream( self, stream_name ) :
		if stream_name == self.__hard_stream :
			raise StreamDeletionException( "Control Stream cannot be deleted!" )
		del self.__streams[ stream_name ]


	def getHardStreamName( self ) :
		return self.__hard_stream


	def setHardStreamName( self, hard_stream ) :
		if hard_stream not in self.__streams :
			raise HardStreamException( "The Stream doesn't exist. Can't harden it." )
		self.__hard_stream = hard_stream


	def getIdentifierForStream( self, stream_name = None, byte_len = 2 ) :
		if stream_name == None :
			stream_name = self.__hard_stream

		assert stream_name in list(self.__streams.keys())
		#print("Inside getIdentifierForStream...the stream name is: %s" % stream_name)
		StandardCyclingKeys = self.__streams[ stream_name ]
		out_StandardCyclingKey = self.__streams[ stream_name ][1]
		#print("Inside getIdentifierForStream...the out_StandardCyclingKey is: %s" % out_StandardCyclingKey)
		ident = out_StandardCyclingKey.xor( self.__comparer[:byte_len], cycle = False )
		#print("Inside getIdentifierForStream...ident is: %s" % ident)

		hardIdentify = (stream_name == self.__hard_stream)
		self.__cycleKey( out_StandardCyclingKey, hardIdentify )

		return ident


	def checkIdentifier( self, bytes_ ) :
		byte_len = len( bytes_ )
		#print("the length of the bytes is: %s" % byte_len)
		for stream_name, StandardCyclingKeys in list(self.__streams.items()) :
			#print("Inside StreamIdentifier checkIdentifier method. For Loop.")
			inp_StandardCyclingKey = StandardCyclingKeys[0]
			#print("Inside checkIdentifier the inp_StandardCyclingKey is : %s" % inp_StandardCyclingKey)
			#print("Inside checkIdentifier the digest of inputStandardCycling Key is: %s" % inp_StandardCyclingKey.digest())
			hardIdentify = (stream_name == self.__hard_stream)

			comparer = self.__comparer[:byte_len] #THIS IS ALWAYS THE VALUE ab. MIGHT BE THE BUG 
			#print("self.__comparer in checkIdentifier is: %s" % self.__comparer)
			plain = inp_StandardCyclingKey.xor( bytes_, cycle = False )
			#print("comparer of checkIdentifier is: %s" % comparer)
			#print("plain result of checkIdentifier is : %s" % plain)
			if plain == comparer :
				#print("plain is equal comparer in checkIdentifier")
				self.__cycleKey( inp_StandardCyclingKey, hardIdentify )
				return stream_name

		return None


	def __cycleKey( self, key, hardIdentify ) :
		if not self.cycle : return
		if not hardIdentify :
			key.cycle()


	def getStreams( self, ) :
		return list(self.__streams.keys())


	def reset( self ) :
		for stream_name, StandardCyclingKeys in list(self.__streams.items()) :
			for key in StandardCyclingKeys :
				key.reset()
