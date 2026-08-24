import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Button from '../components/ui/Button';

describe('Button', () => {
  it('renders its children as visible text', () => {
    render(<Button>Add to ledger</Button>);
    expect(screen.getByText('Add to ledger')).toBeInTheDocument();
  });

  it('calls onClick when clicked', async () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Submit</Button>);

    await userEvent.click(screen.getByText('Submit'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled and unclickable when the disabled prop is set', async () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick} disabled>Submit</Button>);

    const button = screen.getByText('Submit');
    expect(button).toBeDisabled();

    await userEvent.click(button);
    expect(handleClick).not.toHaveBeenCalled();
  });
});
