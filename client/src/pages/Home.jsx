import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { useSearchParams } from "react-router-dom";
import { Rss } from "lucide-react";
import { listContent } from "../services/contentApi";
import ContentCard from "../components/content/ContentCard";
import { ContentCardSkeleton } from "../components/ui/Skeleton";
import EmptyState from "../components/ui/EmptyState";

export default function Home() {
  const categories = useSelector((state) => state.categories.items);
  const subscribedIds = useSelector((state) => state.categories.subscribedIds);
  const [searchParams] = useSearchParams();
  const search = searchParams.get("q") || "";

  const [activeCategory, setActiveCategory] = useState(null);
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    listContent({ categoryId: activeCategory, search })
      .then(setItems)
      .finally(() => setLoading(false));
  }, [activeCategory, search]);

  const recommended = !search && !activeCategory
    ? items.filter((i) => subscribedIds.includes(i.categoryId)).slice(0, 2)
    : [];
  const feedItems = recommended.length ? items.filter((i) => !recommended.includes(i)) : items;

  return (
    <div className="space-y-6">
      {/* Horizontal category tabs, underline-style with the active tab in green */}
      <div className="flex items-center gap-6 overflow-x-auto border-b border-navy-border -mx-1 px-1">
        <button
          onClick={() => setActiveCategory(null)}
          className={`shrink-0 pb-3 text-sm font-medium border-b-2 -mb-px transition ${
            !activeCategory
              ? "border-brand-500 text-brand-600"
              : "border-transparent text-slate-400 hover:text-cream"
          }`}
        >
          All
        </button>
        {categories.map((cat) => (
          <button
            key={cat.id}
            onClick={() => setActiveCategory(cat.id)}
            className={`shrink-0 pb-3 text-sm font-medium border-b-2 -mb-px transition ${
              activeCategory === cat.id
                ? "border-brand-500 text-brand-600"
                : "border-transparent text-slate-400 hover:text-cream"
            }`}
          >
            {cat.name}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="grid sm:grid-cols-2 gap-5">
          {[1, 2, 3, 4].map((i) => (
            <ContentCardSkeleton key={i} />
          ))}
        </div>
      ) : items.length === 0 ? (
        <EmptyState
          icon={Rss}
          title="Nothing here yet"
          description={search ? "Try a different search term or clear filters." : "Be the first to post in this category."}
        />
      ) : (
        <div className="space-y-8">
          {recommended.length > 0 && (
            <section className="space-y-3">
              <p className="text-xs font-medium text-slate-400">Recommended for you</p>
              <div className="grid sm:grid-cols-2 gap-5">
                {recommended.map((item) => (
                  <ContentCard key={item.id} item={item} />
                ))}
              </div>
            </section>
          )}
          <section className="space-y-3">
            <div className="grid sm:grid-cols-2 gap-5">
              {feedItems.map((item) => (
                <ContentCard key={item.id} item={item} />
              ))}
            </div>
          </section>
        </div>
      )}
    </div>
  );
}
