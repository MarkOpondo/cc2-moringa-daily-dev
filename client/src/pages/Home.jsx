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
    ? items.filter((i) => subscribedIds.includes(i.categoryId)).slice(0, 3)
    : [];
  const feedItems = recommended.length ? items.filter((i) => !recommended.includes(i)) : items;

  return (
    <div className="space-y-8">
      <div>
        <p className="text-xs font-mono text-amber-500 mb-1">// feed</p>
        <h1 className="text-2xl font-bold text-white">
          {search ? `Results for "${search}"` : "What the community's sharing"}
        </h1>
      </div>

      <div className="flex gap-2 flex-wrap">
        <button
          onClick={() => setActiveCategory(null)}
          className={`px-3 py-1.5 rounded-full text-xs font-medium border transition ${
            !activeCategory
              ? "bg-amber-500 text-slate-950 border-amber-500"
              : "border-slate-800 text-slate-400 hover:border-slate-700"
          }`}
        >
          All
        </button>
        {categories.map((cat) => (
          <button
            key={cat.id}
            onClick={() => setActiveCategory(cat.id)}
            className={`px-3 py-1.5 rounded-full text-xs font-medium border transition ${
              activeCategory === cat.id
                ? "bg-amber-500 text-slate-950 border-amber-500"
                : "border-slate-800 text-slate-400 hover:border-slate-700"
            }`}
          >
            {cat.name}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
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
              <p className="text-xs font-mono text-slate-500">// recommended for you, based on your subscriptions</p>
              <div className="space-y-3">
                {recommended.map((item) => (
                  <ContentCard key={item.id} item={item} />
                ))}
              </div>
            </section>
          )}
          <section className="space-y-3">
            {recommended.length > 0 && <p className="text-xs font-mono text-slate-500">// everything else</p>}
            <div className="space-y-3">
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
