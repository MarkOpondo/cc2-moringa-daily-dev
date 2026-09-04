import { useEffect, useMemo, useState } from "react";
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
  const [searchParams, setSearchParams] = useSearchParams();
  const search = searchParams.get("q") || "";
  const categoryParam = searchParams.get("category");
  const activeCategory = categoryParam ? Number(categoryParam) : null;
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError("");

    listContent({ categoryId: activeCategory, search })
      .then((data) => {
        if (!cancelled) setItems(data);
      })
      .catch((requestError) => {
        if (!cancelled) {
          setItems([]);
          setError(requestError.message || "Unable to load the feed.");
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [activeCategory, search]);

  const recommended = useMemo(
    () =>
      !search && !activeCategory
        ? items
            .filter((item) =>
              item.categories?.some((category) => subscribedIds.includes(category.id))
            )
            .slice(0, 2)
        : [],
    [activeCategory, items, search, subscribedIds]
  );
  const feedItems = recommended.length
    ? items.filter((item) => !recommended.includes(item))
    : items;

  function selectCategory(categoryId) {
    const next = new URLSearchParams(searchParams);
    if (categoryId) next.set("category", String(categoryId));
    else next.delete("category");
    setSearchParams(next);
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-6 overflow-x-auto border-b border-navy-border -mx-1 px-1">
        <button
          onClick={() => selectCategory(null)}
          className={`shrink-0 pb-3 text-sm font-medium border-b-2 -mb-px transition ${
            !activeCategory
              ? "border-brand-500 text-brand-600"
              : "border-transparent text-slate-400 hover:text-cream"
          }`}
        >
          All
        </button>
        {categories.map((category) => (
          <button
            key={category.id}
            onClick={() => selectCategory(category.id)}
            className={`shrink-0 pb-3 text-sm font-medium border-b-2 -mb-px transition ${
              activeCategory === category.id
                ? "border-brand-500 text-brand-600"
                : "border-transparent text-slate-400 hover:text-cream"
            }`}
          >
            {category.name}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="grid sm:grid-cols-2 gap-5">
          {[1, 2, 3, 4].map((id) => <ContentCardSkeleton key={id} />)}
        </div>
      ) : error ? (
        <EmptyState icon={Rss} title="Unable to load the feed" description={error} />
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
                {recommended.map((item) => <ContentCard key={item.id} item={item} />)}
              </div>
            </section>
          )}
          <section className="grid sm:grid-cols-2 gap-5">
            {feedItems.map((item) => <ContentCard key={item.id} item={item} />)}
          </section>
        </div>
      )}
    </div>
  );
}
