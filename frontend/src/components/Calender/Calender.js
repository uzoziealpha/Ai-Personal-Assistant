import React from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import listPlugin from '@fullcalendar/list';

const Calendar = () => {
  return (
    <div>
      <FullCalendar
        plugins={[dayGridPlugin, listPlugin]}
        initialView="dayGridMonth"
        events={[
          { title: 'Meeting', date: '2023-10-10' },
          { title: 'Event', date: '2023-10-15' },
        ]}
      />
    </div>
  );
};

export default Calendar;