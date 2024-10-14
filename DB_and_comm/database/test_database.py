from unittest import TestCase

from DB_and_comm.database.database import Connection


class TestConnection(TestCase):
    def test_add_job(self):
        connection: Connection = Connection()
        row_id = connection.add_job(1, 1, "Christian", 1, 4, 'PLA', 'Black', 'THIS IS GCODE')

    def test_add_gcode(self):
        connection: Connection = Connection()
        row_id = connection.add_file('THIS IS GCODE')

    def test_get_gcode_from_job_id(self):
        connection: Connection = Connection()
        file_text = connection.get_gcode_from_job_id(1)
        assert file_text == 'THIS IS GCODE'

    def test_add_filament_type(self):
        self.fail()

    def test_get_filament_type_id(self):
        self.fail()

    def test_add_filament_color(self):
        self.fail()

    def test_get_filament_color_id(self):
        self.fail()

    def test_add_manufacturer(self):
        self.fail()

    def test_get_manufacturer_id(self):
        self.fail()

    def test_add_filament(self):
        self.fail()

    def test_get_filament_by_type_and_color(self):
        self.fail()

    def test_update_job_status(self):
        self.fail()

    def test_add_file(self):
        self.fail()

    def test_get_all_jobs_from_status(self):
        self.fail()

    def test_get_gcode_from_file_id(self):
        self.fail()

    def test_add_printer(self):
        self.fail()
