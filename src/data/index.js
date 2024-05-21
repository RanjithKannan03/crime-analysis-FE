import moment from "moment/moment";

export const cardsData = [
  {
    title: "Low Severity Cases",
    change: 24,
    amount: 420,
  },
  {
    title: "Medium Severity Cases",
    change: 14,
    amount: 300,
  },
  {
    title: "High Severity Cases",
    change: 18,
    amount: 200,
  },
  {
    title: "Critical Severity Cases",
    change: 12,
    amount: 500,
  },
];

export const ordersData = [
  {
    name: "Low Severity Cases",
    type: "Illustration",
    items: 58,
    change: 290,
  },
  {
    name: "Medium Severity Cases",
    type: "Illustration",
    items: 12,
    change: 72
  },
  {
    name: "High Severity Cases",
    type: "Illustration",
    items: 7,
    change: 70
  },
  {
    name: "Critical Severity Cases",
    type: "Illustration",
    items: 21,
    change: 15
  }
]


//* get the value in group number format
export const groupNumber = (number) => {
  return parseFloat(number.toFixed(2)).toLocaleString("en", {
    useGrouping: true,
  });
};


//* calendar Events
let eventGuid = 0
let todayStr = moment().format("YYYY-MM-DD")  // YYYY-MM-DD of today
export const INITIAL_EVENTS = [
  {
    id: createEventId(),
    title: 'CM meet',
    start: todayStr + 'T09:00:00',

  },
  {
    id: createEventId(),
    title: 'PM escort',
    start: moment(todayStr).add(1, "days").format("YYYY-MM-DD") + 'T16:00:00'
  },
  {
    id: createEventId(),
    title: "Head meetup",
    start: moment(todayStr).add(2, "days").format("YYYY-MM-DD") + 'T20:00:00'
  },
  {
    id: createEventId(),
    title: "Cyber wing meet",
    start: moment(todayStr).add(3, "days").format("YYYY-MM-DD") + 'T09:00:00'
  },
  {
    id: createEventId(),
    title: "Citizen connect",
    start: moment(todayStr).add(5, "days").format("YYYY-MM-DD") + 'T13:00:00'
  },
  {
    id: createEventId(),
    title: "Awareness rally ",
    start: moment(todayStr).add(6, "days").format("YYYY-MM-DD") + 'T13:00:00'
  },
]

export function createEventId() {
  return String(eventGuid++)
}


// * tasks
export const boardData = {
  columns: [
    {
      id: 1,
      title: "Backlog Cases",
      cards: [
        {
          id: 1,
          title: "Assault in Koramangala",
          description: "Occurred at night, clear weather, high population density"
        },
        {
          id: 2,
          title: "Burglary in Downtown",
          description: "Occurred during the day, cloudy weather, moderate population density"
        },
      ]
    },
    {
      id: 2,
      title: "To Investigate",
      cards: [
        {
          id: 9,
          title: "Robbery in Suburbia",
          description: "Undergoing investigation, night time, rainy weather, low population density",
        }
      ]
    },
    {
      id: 3,
      title: "Investigating",
      cards: [
        {
          id: 10,
          title: "Fraud Scheme",
          description: "Legal proceedings underway, occurred during daytime, clear weather, high population density"
        },
        {
          id: 11,
          title: "Drug Trafficking",
          description: "Case being built, occurred at night, foggy weather, moderate population density"
        }
      ]
    },
    {
      id: 4,
      title: "Completed",
      cards: [
        {
          id: 12,
          title: "Vandalism Incident",
          description: "Case closed, occurred during daytime, clear weather, low population density"
        },

        {
          id: 13,
          title: "Shoplifting Arrest",
          description: "Perpetrator apprehended, occurred at night, rainy weather, high population density"
        }
      ]
    }
  ]
}


// * user table data
export const userData = [
  {
    name: {
      firstName: 'John',
      lastName: 'Doe',
    },
    address: '261 Erdman Ford',
    city: 'East Daphne',
    state: 'Kentucky',
  },
  {
    name: {
      firstName: 'Jane',
      lastName: 'Doe',
    },
    address: '769 Dominic Grove',
    city: 'Columbus',
    state: 'Ohio',
  },
  {
    name: {
      firstName: 'Joe',
      lastName: 'Doe',
    },
    address: '566 Brakus Inlet',
    city: 'South Linda',
    state: 'West Virginia',
  },
  {
    name: {
      firstName: 'Kevin',
      lastName: 'Vandy',
    },
    address: '722 Emie Stream',
    city: 'Lincoln',
    state: 'Nebraska',
  },
  {
    name: {
      firstName: 'Joshua',
      lastName: 'Rolluffs',
    },
    address: '32188 Larkin Turnpike',
    city: 'Charleston',
    state: 'South Carolina',
  }, {
    name: {
      firstName: 'Jane',
      lastName: 'Doe',
    },
    address: '769 Dominic Grove',
    city: 'Columbus',
    state: 'Ohio',
  },
  {
    name: {
      firstName: 'Joe',
      lastName: 'Doe',
    },
    address: '566 Brakus Inlet',
    city: 'South Linda',
    state: 'West Virginia',
  },
  {
    name: {
      firstName: 'Kevin',
      lastName: 'Vandy',
    },
    address: '722 Emie Stream',
    city: 'Lincoln',
    state: 'Nebraska',
  },
  {
    name: {
      firstName: 'Joshua',
      lastName: 'Rolluffs',
    },
    address: '32188 Larkin Turnpike',
    city: 'Charleston',
    state: 'South Carolina',
  },
]
