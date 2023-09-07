

/* -------------------------------------------------------------------------- */
/*                                    Utils                                   */
/* -------------------------------------------------------------------------- */
const docReady = fn => {
  // see if DOM is already available
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', fn);
  } else {
    setTimeout(fn, 1);
  }
};

const resize = fn => window.addEventListener('resize', fn);

const isIterableArray = array => Array.isArray(array) && !!array.length;

const camelize = str => {
  const text = str.replace(/[-_\s.]+(.)?/g, (_, c) => (c ? c.toUpperCase() : ''));
  return `${text.substr(0, 1).toLowerCase()}${text.substr(1)}`;
};

const getData = (el, data) => {
  try {
    return JSON.parse(el.dataset[camelize(data)]);
  } catch (e) {
    return el.dataset[camelize(data)];
  }
};

/* ----------------------------- Colors function ---------------------------- */

const hexToRgb = hexValue => {
  let hex;
  hexValue.indexOf('#') === 0 ? (hex = hexValue.substring(1)) : (hex = hexValue);
  // Expand shorthand form (e.g. "03F") to full form (e.g. "0033FF")
  const shorthandRegex = /^#?([a-f\d])([a-f\d])([a-f\d])$/i;
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(
    hex.replace(shorthandRegex, (m, r, g, b) => r + r + g + g + b + b)
  );
  return result
    ? [parseInt(result[1], 16), parseInt(result[2], 16), parseInt(result[3], 16)]
    : null;
};

const rgbaColor = (color = '#fff', alpha = 0.5) => `rgba(${hexToRgb(color)}, ${alpha})`;

/* --------------------------------- Colors --------------------------------- */

const getColor = (name, dom = document.documentElement) =>
  getComputedStyle(dom).getPropertyValue(`--falcon-${name}`).trim();

const getColors = dom => ({
  primary: getColor('primary', dom),
  secondary: getColor('secondary', dom),
  success: getColor('success', dom),
  info: getColor('info', dom),
  warning: getColor('warning', dom),
  danger: getColor('danger', dom),
  light: getColor('light', dom),
  dark: getColor('dark', dom)
});

const getSoftColors = dom => ({
  primary: getColor('soft-primary', dom),
  secondary: getColor('soft-secondary', dom),
  success: getColor('soft-success', dom),
  info: getColor('soft-info', dom),
  warning: getColor('soft-warning', dom),
  danger: getColor('soft-danger', dom),
  light: getColor('soft-light', dom),
  dark: getColor('soft-dark', dom)
});

const getGrays = dom => ({
  white: getColor('white', dom),
  100: getColor('100', dom),
  200: getColor('200', dom),
  300: getColor('300', dom),
  400: getColor('400', dom),
  500: getColor('500', dom),
  600: getColor('600', dom),
  700: getColor('700', dom),
  800: getColor('800', dom),
  900: getColor('900', dom),
  1000: getColor('1000', dom),
  1100: getColor('1100', dom),
  black: getColor('black', dom)
});

const hasClass = (el, className) => {
  !el && false;
  return el.classList.value.includes(className);
};

const addClass = (el, className) => {
  el.classList.add(className);
};

const getOffset = el => {
  const rect = el.getBoundingClientRect();
  const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
  return { top: rect.top + scrollTop, left: rect.left + scrollLeft };
};

function isScrolledIntoView(el) {
  const rect = el.getBoundingClientRect();
  const windowHeight = window.innerHeight || document.documentElement.clientHeight;
  const windowWidth = window.innerWidth || document.documentElement.clientWidth;

  const vertInView = rect.top <= windowHeight && rect.top + rect.height >= 0;
  const horInView = rect.left <= windowWidth && rect.left + rect.width >= 0;

  return vertInView && horInView;
}

const breakpoints = {
  xs: 0,
  sm: 576,
  md: 768,
  lg: 992,
  xl: 1200,
  xxl: 1540
};

const getBreakpoint = el => {
  const classes = el && el.classList.value;
  let breakpoint;
  if (classes) {
    breakpoint =
      breakpoints[
        classes
          .split(' ')
          .filter(cls => cls.includes('navbar-expand-'))
          .pop()
          .split('-')
          .pop()
      ];
  }
  return breakpoint;
};

/* --------------------------------- Cookie --------------------------------- */

const setCookie = (name, value, expire) => {
  const expires = new Date();
  expires.setTime(expires.getTime() + expire);
  document.cookie = name + '=' + value + ';expires=' + expires.toUTCString();
};

const getCookie = name => {
  var keyValue = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
  return keyValue ? keyValue[2] : keyValue;
};

const settings = {
  tinymce: {
    theme: 'oxide'
  },
  chart: {
    borderColor: 'rgba(255, 255, 255, 0.8)'
  }
};

/* -------------------------- Chart Initialization -------------------------- */

const newChart = (chart, config) => {
  const ctx = chart.getContext('2d');
  return new window.Chart(ctx, config);
};

/* ---------------------------------- Store --------------------------------- */

const getItemFromStore = (key, defaultValue, store = localStorage) => {
  try {
    return JSON.parse(store.getItem(key)) || defaultValue;
  } catch {
    return store.getItem(key) || defaultValue;
  }
};

const setItemToStore = (key, payload, store = localStorage) => store.setItem(key, payload);
const getStoreSpace = (store = localStorage) =>
  parseFloat((escape(encodeURIComponent(JSON.stringify(store))).length / (1024 * 1024)).toFixed(2));

/* get Dates between */

const getDates = (startDate, endDate, interval = 1000 * 60 * 60 * 24) => {
  const duration = endDate - startDate;
  const steps = duration / interval;
  return Array.from({ length: steps + 1 }, (v, i) => new Date(startDate.valueOf() + interval * i));
};

const getPastDates = duration => {
  let days;

  switch (duration) {
    case 'week':
      days = 7;
      break;
    case 'month':
      days = 30;
      break;
    case 'year':
      days = 365;
      break;

    default:
      days = duration;
  }

  const date = new Date();
  const endDate = date;
  const startDate = new Date(new Date().setDate(date.getDate() - (days - 1)));
  return getDates(startDate, endDate);
};

/* Get Random Number */
const getRandomNumber = (min, max) => {
  return Math.floor(Math.random() * (max - min) + min);
};




// Funciones del archivo echarts-util.js

const getPosition = (pos, params, dom, rect, size) => ({
  top: pos[1] - size.contentSize[1] - 10,
  left: pos[0] - size.contentSize[0] / 2
});

const echartSetOption = (chart, userOptions, getDefaultOptions) => {
  const themeController = document.body;
  // Merge user options with lodash
  chart.setOption(window._.merge(getDefaultOptions(), userOptions));

  themeController.addEventListener('clickControl', ({ detail: { control } }) => {
    if (control === 'theme') {
      chart.setOption(window._.merge(getDefaultOptions(), userOptions));
    }
  });
};



/* -------------------------------------------------------------------------- */
/*                                Total Order                                 */
/* -------------------------------------------------------------------------- */

const totalOrderInit = () => {
const ECHART_LINE_TOTAL_ORDER = '.echart-line-total-order';

//
// ─── TOTAL ORDER CHART ──────────────────────────────────────────────────────────
//
const $echartLineTotalOrder = document.querySelector(ECHART_LINE_TOTAL_ORDER);
if ($echartLineTotalOrder) {
  // Get options from data attribute
  const userOptions = utils.getData($echartLineTotalOrder, 'options');
  const chart = window.echarts.init($echartLineTotalOrder);

  // Default options
  const getDefaultOptions = () => ({
    tooltip: {
      triggerOn: 'mousemove',
      trigger: 'axis',
      padding: [7, 10],
      formatter: '{b0}: {c0}',
      backgroundColor: utils.getGrays()['100'],
      borderColor: utils.getGrays()['300'],
      textStyle: { color: utils.getColors().dark },
      borderWidth: 1,
      transitionDuration: 0,
      position(pos, params, dom, rect, size) {
        return getPosition(pos, params, dom, rect, size);
      },
    },
    xAxis: {
      type: 'category',
      data: ['Week 4', 'Week 5', 'week 6', 'week 7'],
      boundaryGap: false,
      splitLine: { show: false },
      axisLine: {
        show: false,
        lineStyle: {
          color: utils.getGrays()['300'],
          type: 'dashed',
        },
      },
      axisLabel: { show: false },
      axisTick: { show: false },
      axisPointer: { type: 'none' },
    },
    yAxis: {
      type: 'value',
      splitLine: { show: false },
      axisLine: { show: false },
      axisLabel: { show: false },
      axisTick: { show: false },
      axisPointer: { show: false },
    },
    series: [
      {
        type: 'line',
        lineStyle: {
          color: utils.getColors().primary,
          width: 3,
        },
        itemStyle: {
          color: utils.getGrays().white,
          borderColor: utils.getColors().primary,
          borderWidth: 2,
        },
        hoverAnimation: true,
        data: [20, 40, 100, 120],
        // connectNulls: true,
        smooth: 0.6,
        smoothMonotone: 'x',
        showSymbol: false,
        symbol: 'circle',
        symbolSize: 8,
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              {
                offset: 0,
                color: utils.rgbaColor(utils.getColors().primary, 0.25),
              },
              {
                offset: 1,
                color: utils.rgbaColor(utils.getColors().primary, 0),
              },
            ],
          },
        },
      },
    ],
    grid: {
      bottom: '2%',
      top: '0%',
      right: '10px',
      left: '10px',
    },
  });

  echartSetOption(chart, userOptions, getDefaultOptions);
}
};

docReady(totalOrderInit);

