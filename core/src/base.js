'use strict';

import './css/base.css';
import './bulma.js';
import './fontawesome.js';

// favicon
import favicon from './img/rocket-solid.svg';
const link = document.createElement('link');
link.rel = 'shortcut icon';
link.href = favicon;
document.head.appendChild(link);
