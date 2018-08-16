import hashlib
import pyzwave
from cc_c import sizeInBits

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


class CodeGeneratorZwave():

    WKECO_COMM_ECOCOMMAND   = 0x20
    WKECO_COMM_ECOCOMMAND_R = 0x21

    WKECO_REPLY_OK          = 0x01 # Packet received, still waiting for the rest of the capsule
    WKECO_REPLY_EXECUTED    = 0x02 # Packet received. Capsule was executed and reply contains return value in the following bytes. Sent after first or last message.
    WKECO_REPLY_TOO_BIG     = 0x03 # Capsule is too big to fit in the capsule file. TODONR: not used yet.


    MAX_PAYLOAD = 0x4

    seqnr = 0

    # Messages to Darjeeling should have a command. The reply command is response+1 (by convention)
    # 0x88 is the zwave proprietary command, which is received by wkcomm on the node.
    # Format:
    #    Request:  [ 0x88, 0x20 (ECOCOMMAND),   seq_LSB, seq_MSB, packetnr, lastpacketnr, retval_size, payload.... ]
    #    Response: [ 0x88, 0x21 (ECOCOMMAND_R), seq_LSB, seq_MSB, retval.... ]

    def __init__(self, com_port):
      pyzwave.init(com_port)

    def send(self, code, retval_type, destination_id):
        code_sha1 = hashlib.sha1(bytearray(code)).digest()
        code_hash = [ord(i) for i in code_sha1[-4:]]
        code_padding = [0] if len(code) % 2 == 1 else 0 # Make sure the capsule has even length
        capsule_length = 2 + len(code_hash) + len(code) + len(code_padding)
        capsule = [capsule_length % 256, (capsule_length >> 8) % 256] + code_hash + code + code_padding

        retval_size = sizeInBits(retval_type) / 8
        capsule_fragments = list(chunks(capsule, CodeGeneratorZwave.MAX_PAYLOAD))
        number_of_fragments = len(capsule_fragments)
        # print "Return type " + str(retval_type)
        # print "Return size " + str(retval_size)
        # print "Executing capsule", capsule
        for i in range(number_of_fragments):
            message = [0x88,
                        CodeGeneratorZwave.WKECO_COMM_ECOCOMMAND,
                        CodeGeneratorZwave.seqnr%256,
                        CodeGeneratorZwave.seqnr/256,
                        i,
                        number_of_fragments-1,
                        retval_size] + capsule_fragments[i]
            # print "Fragment ", capsule_fragments[i]
            # print "Message ", message
            pyzwave.send(destination_id, message)
            reply = pyzwave.receive(1000)
            if (reply[1][3] == CodeGeneratorZwave.WKECO_REPLY_TOO_BIG):
                raise OutOfMemoryError("Capsule too big to fit in the node's buffer")
            if (reply[1][3] == CodeGeneratorZwave.WKECO_REPLY_EXECUTED):
                # print "Received reply after executing capsule:" + str(reply)
                return bytearray(reply[1][4:])

