import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import ContentCard from '../components/content/ContentCard';

const mockItem = {
  id: 'n1',
  title: 'What I wish I knew before my first backend interview',
  body: 'Landing a backend role is about more than syntax.',
  type: 'article',
  status: 'approved',
  createdAt: new Date().toISOString(),
  category: { id: 'c4', name: 'Backend' },
  author: { id: 'u2', username: 'brian_writes', role: 'tech_writer' },
  thumbnail: 'https://picsum.photos/seed/n1/600/400',
  readTime: '6 min read',
  likes: 3,
};

function renderCard(props = {}) {
  return render(
    <MemoryRouter>
      <ContentCard item={{ ...mockItem, ...props }} />
    </MemoryRouter>
  );
}

describe('ContentCard', () => {
  it('renders the title, category, and author', () => {
    renderCard();
    expect(screen.getByText(mockItem.title)).toBeInTheDocument();
    expect(screen.getByText('Backend')).toBeInTheDocument();
    expect(screen.getByText('brian_writes')).toBeInTheDocument();
  });

  it('links to the correct content detail page', () => {
    renderCard();
    const link = screen.getByRole('link');
    expect(link).toHaveAttribute('href', '/content/n1');
  });

  it('shows the content type as a tag', () => {
    renderCard({ type: 'video' });
    expect(screen.getByText('Video')).toBeInTheDocument();
  });

  it('shows duration for video/audio and read time for articles', () => {
    const { rerender } = render(
      <MemoryRouter>
        <ContentCard item={{ ...mockItem, type: 'video', duration: '45m', readTime: undefined }} />
      </MemoryRouter>
    );
    expect(screen.getByText('45m')).toBeInTheDocument();

    rerender(
      <MemoryRouter>
        <ContentCard item={{ ...mockItem, type: 'article', readTime: '6 min read' }} />
      </MemoryRouter>
    );
    expect(screen.getByText('6 min read')).toBeInTheDocument();
  });

  it('shows a status badge for non-approved content', () => {
    renderCard({ status: 'pending' });
    expect(screen.getByText('pending')).toBeInTheDocument();
  });
});
