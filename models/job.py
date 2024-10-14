from sqlalchemy import RowMapping, Sequence


def get_job_list(rows: Sequence[RowMapping]) -> list['Job']:
    job_list = []
    for row in rows:
        job = Job(
            order_id=row['order_id'],
            quantity=row['quantity'],
            job_name=row['job_name'],
            printer_assignment=row['printer_assignment'],
            nozzle_size=row['nozzle_size'],
            filament_type=row['filament_type'],
            filament_color=row['color'],
            file_text=row['file_text']
        )
        job_list.append(job)
    return job_list


class Job:

    def __init__(self, order_id: int, quantity: int, job_name: str, printer_assignment: int | None, nozzle_size: int,
                 filament_type: str, filament_color: str, file_text: str):
        self.order_id = order_id
        self.quantity = quantity
        self.job_name = job_name
        self.printer_assignment = printer_assignment
        self.nozzle_size = nozzle_size
        self.filament_type = filament_type
        self.filament_color = filament_color
        self.file_text = file_text

