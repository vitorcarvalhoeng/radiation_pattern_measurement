from mock_serial import MockSerial
from serial import Serial


def gcode_positioner():
    device_mock = MockSerial()
    device_mock.stub(
        receive_bytes=b'G',
        send_bytes=b'ok\n'
    )

    device_mock.stub(
        receive_bytes=b'M',
        send_bytes=b'ok\n'
    )


    device_mock.open()
    ser = Serial(device_mock.port)

    return ser, device_mock

