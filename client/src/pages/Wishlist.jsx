import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { Bookmark } from "lucide-react";
import { listWishlist } from "../services/contentApi";
import { selectCurrentUser } from "../features/auth/authSlice";
import ContentCard from "../components/content/ContentCard";
import { ContentCardSkeleton } from "../components/ui/Skeleton";
import EmptyState from "../components/ui/EmptyState";
import Button from "../components/ui/Button";
import { Link } from "react-router-dom";

export default function Wishlist() {
  const user = useSelector(selectCurrentUser);
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user?.id) return;
    listWishlist(user.id).then((data) => {
      setItems(data);
      setLoading(false);
    });
  }, [user?.id]);

  return (
    <div className="space-y-6">
      <div>
        <p className="text-xs font-mono text-amber-500 mb-1">// wishlist</p>
        <h1 className="text-2xl font-bold text-white">Saved for later</h1>
      </div>

      {loading ? (
        <div className="space-y-3">
          <ContentCardSkeleton />
          <ContentCardSkeleton />
        </div>
      ) : items.length === 0 ? (
        <EmptyState
          icon={Bookmark}
          title="Nothing saved yet"
          description="Tap Save on any post to keep it here for later."
          action={
            <Link to="/">
              <Button size="sm">Browse the feed</Button>
            </Link>
          }
        />
      ) : (
        <div className="space-y-3">
          {items.map((item) => (
            <ContentCard key={item.id} item={item} />
          ))}
        </div>
      )}
    </div>
  );
}
