# from mock_serial import MockSerial
# from serial import Serial
# import dummyserial as ds
import mock

def gcode_positioner():
    # device_mock = MockSerial()
    # device_mock.stub(
    #     receive_bytes=b'G',
    #     send_bytes=b'ok\n'

    # )

    # device_mock.stub(
    #     receive_bytes=b'M',
    #     send_bytes=b'ok\n'
    # )


    # device_mock.open()
    # ser = Serial(device_mock.port,timeout=3)
    




    # ser = ds.Serial('1',timeout=3)
    # ds.DEFAULT_RESPONSE= b'ok\n'
    
    # return ser, device_mock


    ser = mock.Mock()
    ser.readline = mock.Mock(return_value="ok\n".encode())


    return ser

