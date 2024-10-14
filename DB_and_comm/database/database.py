import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import *


class Connection:
    """
    This class contains all information required to open a connection to a database.
    It makes use of environment variables:
        - POSTGRES_USER | Defaults to "postgres" if not specified
        - POSTGRES_DB   | Defaults to "postgres" if not specified
        - POSTGRES_PORT | Defaults to 5432 if not specified
        - POSTGRES_HOST
        - POSTGRES_PASSWORD
    """

    def __init__(self):
        load_dotenv(find_dotenv())
        username: str = os.getenv("POSTGRES_USER")
        database: str = os.getenv("POSTGRES_DB")
        port: str = os.getenv("POSTGRES_PORT")
        host: str = os.getenv("POSTGRES_HOST")
        password: str = os.getenv("POSTGRES_PASSWORD")
        print(username)
        if port is None:
            port = "5432"

        if database is None:
            database = "postgres"

        if username is None:
            username = "postgres"
        connection_string: str = f'postgresql://{username}:{password}@{host}:{port}/{database}'
        self.engine = create_engine(connection_string, pool_size=1)
        self.meta_data = MetaData()





    # =================== FILAMENT STUFF ===================
    def add_filament_type(self, filament_type: str):
        """
        Adds a filament type to the filament table in the database
        :param filament_type: String, name of filament type
        """
        try:
            t = Table("filament_types", self.meta_data, autoload_with=self.engine)
            stmt = insert(t).values(filament_type=filament_type)

            with self.engine.connect() as db_connection:
                result = db_connection.execute(stmt)
                db_connection.commit()
                row = result.inserted_primary_key
                if row is not None:
                    return int(row[0])
                return None
        except Exception as e:
            print(f"Issue adding new filament type: {e}")

    def get_filament_type_id(self, filament_type: str) -> int | None:
        """
        Fetches the id for any given filament based off filament type
        :param filament_type: String, filament type you wish to get the id of
        :return: int of filament id or `None`
        """
        try:
            t = Table("filament_types", self.meta_data, autoload_with=self.engine)
            stmt = select(t).where(t.c.filament_type == filament_type)
            with self.engine.connect() as db_connection:
                result = db_connection.execute(stmt)
                row = result.fetchone()
                if row is not None:
                    return int(row[0])
                return None
        except Exception as e:
            print(f"Issue querying database: {e}")

    def add_filament_color(self, color: str) -> int | None:
        """
        Adds a filament color to the color table in the database
        :param color: str - Examples would be "blue"
        :returns: int | None - Either the primary key of the row that was successfully inserted or None
        """
        try:
            t = Table("filament_colors", self.meta_data, autoload_with=self.engine)
            stmt = insert(t).values(color=color)
            with self.engine.connect() as db_connection:
                print(db_connection.info)
                result = db_connection.execute(stmt)
                db_connection.commit()
                row = result.inserted_primary_key
                if row is not None:
                    return int(row[0])
                return None
        except Exception as e:
            print(f"Issue adding new filament color: {e}")
            return None

    def get_filament_color_id(self, filament_color: str) -> int | None:
        """
        Fetches id of specified filament color
        :param filament_color:
        :return: int on successfully color id acquisition or None
        """

        try:
            t = Table("filament_colors", self.meta_data, autoload_with=self.engine)
            stmt = select(t).where(t.c.color == filament_color)

            with self.engine.connect() as db_connection:
                result = db_connection.execute(stmt)
                row = result.fetchone()
                if row is not None:
                    return int(row[0])
                return None
        except Exception as e:
            print(f"Issue querying database: {e}")

    def add_manufacturer(self, name: str) -> int | None:
        """
        Adds a filament manufacturer name to the filament table in the database
        :param name: str - Name of the manufacturer
        :returns: int, id of newly added manufacturer or None
        """
        try:
            t = Table("manufacturer", self.meta_data, autoload_with=self.engine)
            stmt = insert(t).values(name=name)

            with self.engine.connect() as db_connection:
                result = db_connection.execute(stmt)  # Begins trasaction
                db_connection.commit()  # Ends transaction
                row = result.inserted_primary_key
                if row is not None:
                    return int(row[0])
                return None
        except Exception as e:
            print(f"Issue adding new filament manufacturer name: {e}")
            return None

    def get_manufacturer_id(self, name: str) -> int | None:
        """
        Gets id for specified manufacturer
        :param name: Name of manufacturer whose id you wish to aquire
        :return: id of manufactuer or None
        """
        try:
            t = Table("manufacturer", self.meta_data, autoload_with=self.engine)
            stmt = select(t).where(t.c.name == name)

            with self.engine.connect() as db_connection:
                result = db_connection.execute(stmt)
                row = result.fetchone()
                if row is not None:
                    return int(row[0])
                return None
        except Exception as e:
            print(f"Issue querying database: {e}")

    def add_filament(self, filament_type: str, color: str, manufacturer: str) -> int | None:
        """
        Adds entire filament to table
        :param filament_type: Type of filament, "PLA", "ABS"
        :param color: Color of filament
        :param manufacturer: Name of manufacturer
        :return: int | None in case where it would not add filament
        """
        try:
            # Query first, then check and reset values
            type_id = self.get_filament_type_id(filament_type)
            color_id = self.get_filament_color_id(color)
            manufacturer_id = self.get_manufacturer_id(manufacturer)

            if type_id is None:
                self.add_filament_type(filament_type)
                type_id = self.get_filament_type_id(filament_type)

            if color_id is None:
                self.add_filament_color(color)
                color_id = self.get_filament_color_id(color)

            if manufacturer_id is None:
                self.add_manufacturer(manufacturer)
                manufacturer_id = self.get_manufacturer_id(manufacturer)

            print(f"VALUES: {type_id}, {color_id}, {manufacturer_id}")

            t = Table("filaments", self.meta_data, autoload_with=self.engine)
            stmt = insert(t).values(filament_type=type_id, filament_color=color_id,
                                    filament_manufacturer=manufacturer_id)
            with self.engine.connect() as db_connection:
                result = db_connection.execute(stmt)
                db_connection.commit()
                row = result.inserted_primary_key
                if row is not None:
                    return int(row[0])
                return None

        except Exception as e:
            print(f"Issue adding filament: {e}")

    def get_filament_by_type_and_color(self, filament_type: str, filament_color: str) -> int | None:
        """
        Gets any filament based off type and color
        :param filament_type:
        :param filament_color:
        :return: Filament id or None
        """
        try:
            filament_type_id = self.get_filament_type_id(filament_type)
            filament_color_id = self.get_filament_color_id(filament_color)

            if filament_type_id is None or filament_color_id is None:
                return None

            t = Table("filaments", self.meta_data, autoload_with=self.engine)
            stmt = select(t).where(and_(t.c.filament_id == filament_type_id, t.c.filament_color == filament_color_id))
            with self.engine.connect() as db_connection:
                result = db_connection.execute(stmt)
                row = result.fetchone()
                if row is not None:
                    return int(row[0])
                return None
        except Exception as e:
            print(f"Could not query for filament id: {e}")
# ===================================================================











    def add_job(self, order_id: int, quantity: int, job_name: str, printer_assignment: int, nozzle_size: int,
                filament_type: str,
                filament_color: str, file_text: str) -> int | None:
        """
        Adds a job to the jobs table
        :param quantity:
        :param file_text: Raw file text for the job, this is most likely sliced gcode
        :param order_id:
        :param job_name:
        :param printer_assignment:
        :param nozzle_size:
        :param filament_type:
        :param filament_color:
        :return int | None: Either returns the row id of the recently added job, or None otherwise
        """
        try:
            # Add file to gcode
            gcode_id = self.add_file(file_text)

            # Check to make sure proper filament first
            filament_id = self.get_filament_by_type_and_color(filament_type, filament_color)

            t = Table("jobs", self.meta_data, autoload_with=self.engine)
            stmt = insert(t).values(order_id=order_id, quantity=quantity, job_name=job_name,
                                    printer_assignment=printer_assignment,
                                    nozzle_size=nozzle_size, filament_id=filament_id, file_id=gcode_id)
            with self.engine.connect() as db_connection:
                result = db_connection.execute(stmt)
                db_connection.commit()
                row = result.inserted_primary_key
                if row is not None:
                    return int(row[0])
                return None
        except Exception as e:
            print(f"Failed to insert into jobs table: {e}")

    def update_job_status(self, order_id: int, status: str) -> int | None:
        """
        Updates the status of job by order id
        :param order_id: Order id of order you with to update the status of
        :param status:
        :return:
        """
        try:
            t = Table("jobs", self.meta_data, autoload_with=self.engine)
            stmt = update(t).where(t.c.order_id == order_id).values(job_status=status)
            with self.engine.connect() as db_connection:
                result = db_connection.execute(stmt)
                db_connection.commit()
                row = result.inserted_primary_key
                if row is not None:
                    return int(row[0])
                return None
        except Exception as e:
            print(f"Failed to update job: {e}")

    def add_file(self, file_text: str) -> int | None:
        """
        Adds a new gcode file to the gcode file table
        :param file_text: Raw gcode file
        :return: int | None - Returns row number (key) on success and None if unable to insert row
        """
        try:
            t = Table("gcode_files", self.meta_data, autoload_with=self.engine)
            stmt = insert(t).values(gcode_text=file_text)

            with self.engine.connect() as db_connection:
                result = db_connection.execute(stmt)
                db_connection.commit()
                row = result.inserted_primary_key
                if row is not None:
                    return int(row[0])
                return None
        except Exception as e:
            print(f"Failed to add gcode to database: {e}")


    def get_all_jobs_from_status(self, status: str) -> Sequence[RowMapping] | None:
        """
        Returns all jobs given a certain status
        :param status:
        :return:
        """
        try:
            t = Table("job_info", self.meta_data, autoload_with=self.engine)
            stmt = select(t).where(t.c.job_status == status)
            with self.engine.connect() as db_connection:
                result = db_connection.execute(stmt)
                result_as_dict = result.mappings().all()
                if result_as_dict is not None:
                    print(result_as_dict)
                    #job_list = get_job_list(result_as_dict)
                    #return job_list
                return None
        except Exception as e:
            print(f"Failed to query for jobs: {e}")

    def get_gcode_from_file_id(self, file_id: int) -> str | None:
        """
        Return raw gcode file from a given file id
        :param file_id:
        :return:
        """
        try:
            t = Table("gcode_files", self.meta_data, autoload_with=self.engine)
            stmt = select(t.c.gcode_text).where(t.c.file_id == file_id)
            with self.engine.connect() as db_connection:
                result = db_connection.execute(stmt)
                row = result.fetchone()
                if row is not None:
                    return str(row[0])
                return None
        except Exception as e:
            print(f"Issue fetching file: {e}")

    def get_gcode_from_job_id(self, job_id: int) -> str | None:
        """
        Returns Gcode associated with any given job id
        :param job_id:
        :return:
        """
        try:
            t = Table("jobs", self.meta_data, autoload_with=self.engine)
            stmt = select(t.c.file_id).where(t.c.job_id == job_id)
            with self.engine.connect() as db_connection:
                result = db_connection.execute(stmt)
                row = result.fetchone()[0]
                if result is not None:
                    return self.get_gcode_from_file_id(row)
                return None
        except Exception as e:
            print(f"Failed to query for jobs: {e}")

    def add_printer(self, printer_id: str, filament_type: str | None, filament_color: str | None, port: int,
                    api_key: str) -> int | None:
        """
        Adds a printer to the database
        :param printer_id:
        :param filament_type:
        :param filament_color:
        :param port:
        :param api_key:
        :return:
        """
        try:
            filament_id = self.get_filament_by_type_and_color(filament_type, filament_color)
            t = Table("printers", self.meta_data, autoload_with=self.engine)
            stmt = insert(t).values(printer_id=printer_id, filament=filament_id, port=port, api_key=api_key)
            with self.engine.connect() as db_connection:
                result = db_connection.execute(stmt)
                pk = result.inserted_primary_key
                if pk is not None:
                    return int(pk[0])
                return None
        except Exception as e:
            print(f"Failed to add printer: {e}")

    def add_printer_file(self, file_text: str, printer_id: int) -> int | None:
        try:
            t = Table("printer_file", self.meta_data, autoload_with=self.engine)
            stmt = insert(t).values(printer_id=printer_id, file_contents=file_text)
            with self.engine.connect() as db_connection:
                result = db_connection.execute(stmt)
                pk = result.inserted_primary_key
                if pk is not None:
                    return int(pk[0])
                return None
        except Exception as e:
            print(f"Failed to add printer configuration file: {e}")
