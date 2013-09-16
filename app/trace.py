class Trace(object):
    
    max_buffer_size = 500
    buffer1 = []
    buffer2 = []
    active_buffer = buffer1
    inactive_buffer = buffer2
    active_buffer_num = 1
    
    def __init__(self, count, position, retrace=False):
        self.count = count
        self.position = position
        self.retrace = retrace
        
    def record(self):
        Trace.active_buffer.append(self)
        Trace.manage_buffers()
    
    @classmethod
    def manage_buffers(self):
        if len(Trace.active_buffer) == Trace.max_buffer_size:
            if Trace.active_buffer_num == 1:
                Trace.active_buffer_num = 2            
                Trace.active_buffer = buffer2
                Trace.inactive_buffer = buffer1
            elif Trace.active_buffer_num == 2:
                Trace.active_buffer_num = 1
                Trace.active_buffer = buffer1
                Trace.inactive_buffer = buffer2
            Trace.active_buffer = []
            
    @classmethod
    def get_trace(self):
        previous_buffer_index = Trace.max_buffer_size - len(Trace.active_buffer)
        trace_record = Trace.inactive_buffer[-previous_buffer_index:]
        trace_record.extend(Trace.active_buffer)
    
    
    
