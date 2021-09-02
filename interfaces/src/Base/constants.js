const colors = {
  secondary: '#FFFCF2',
  primary: '#1890ff',
  tertiary: '#001529',
  background: '#fff',
  error: 'red',
  yellow: '#ffcf71',
};

const naming = {
  greek: 'Τειρεσίας',
  lat: 'Teiresias',
  laut: '/taɪˈriːsiəs/',
};

const evaluation = {
  metric: ({ numberOfEntities, hasDataMatches, meanProximities }) =>
    Math.min(1, numberOfEntities) * Math.max(hasDataMatches, meanProximities),
};

const personalDataMessage = 'Personal Data has been found.';

export { colors, naming, evaluation, personalDataMessage };
