import { render, screen } from '@testing-library/react';
import CoverFitnessApp from '../CoverFitnessApp';

test('renders app title', () => {
  render(<CoverFitnessApp />);
  const heading = screen.getByText(/AI Fitness Assistant/i);
  expect(heading).toBeInTheDocument();
});
