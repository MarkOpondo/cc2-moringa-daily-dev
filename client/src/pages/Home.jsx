import { useEffect, useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { useSearchParams } from "react-router-dom";
import { Rss } from "lucide-react";
import { listContent } from "../services/contentApi";
import { fetchCategories } from "../features/categories/categoriesSlice";
import ContentCard from "../components/content/ContentCard";
import { ContentCardSkeleton } from "../components/ui/Skeleton";
import EmptyState from "../components/ui/EmptyState";

export default function Home() {
  const dispatch = useDispatch();
  const categories = useSelector((state) => state.categories.items || []);
  const subscribedIds = useSelector((state) => state.categories.subscribedIds || []);
  const [searchParams] = useSearchParams();
  const search = searchParams.get("q") || "";

  const [activeCategory, setActiveCategory] = useState(null);
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch categories from backend on component mount
  useEffect(() => {
    dispatch(fetchCategories());
  }, [dispatch]);

  // Fetch public content items whenever search query or selected category changes
  useEffect(() => {
    setLoading(true);
    listContent({ categoryId: activeCategory, search })
      .then((data) => setItems(Array.isArray(data) ? data : []))
      .catch(() => setItems([]))
      .finally(() => setLoading(false));
  }, [activeCategory, search]);

  const recommended = !search && !activeCategory
    ? items.filter((i) => {
        const catId = i.categoryId ?? i.category_id ?? i.CategoryID;
        return subscribedIds.includes(catId);
      }).slice(0, 2)
    : [];
    
  const feedItems = recommended.length 
    ? items.filter((i) => !recommended.includes(i)) 
    : items;

  return (
    <div className="space-y-6">
      {/* Hero band — peach → coral gradient with a curved bottom edge,
          mirroring moringaschool.com's homepage hero. */}
      <div className="relative -mx-4 sm:-mx-6 -mt-6 px-4 sm:px-6 pt-10 pb-16 overflow-hidden bg-gradient-to-b from-hero-from via-hero-via to-hero-to">
        <h1 className="text-2xl sm:text-3xl text-navy max-w-2xl">
          What's new in tech today
        </h1>
        <p className="text-navy/70 text-sm sm:text-base max-w-xl mt-2">
          Articles, videos, and advice from the Moringa School community — alumni, staff, and industry experts.
        </p>
        <svg
          className="absolute -bottom-px left-0 w-full text-paper"
          viewBox="0 0 1440 60"
          preserveAspectRatio="none"
          aria-hidden="true"
        >
          <path fill="currentColor" d="M0,32 C360,64 1080,0 1440,32 L1440,60 L0,60 Z" />
        </svg>
      </div>

      {/* Category filter pills — rounded chips like moringaschool.com's
          course-type selector (Software Engineering / Data / Cyber…). */}
      <div className="flex items-center gap-3 overflow-x-auto -mx-1 px-1 py-1">
        <button
          onClick={() => setActiveCategory(null)}
          className={`shrink-0 px-5 py-2 rounded-full text-sm font-semibold border transition ${
            !activeCategory
              ? "border-brand-500 text-brand-600 bg-white"
              : "border-line text-navy/60 bg-white hover:border-navy/30 hover:text-navy"
          }`}
        >
          All
        </button>
        {categories.map((cat) => {
          const categoryId = cat.id ?? cat.CategoryID;
          const categoryName = cat.name ?? cat.Name;
          return (
            <button
              key={categoryId}
              onClick={() => setActiveCategory(categoryId)}
              className={`shrink-0 px-5 py-2 rounded-full text-sm font-semibold border transition ${
                activeCategory === categoryId
                  ? "border-brand-500 text-brand-600 bg-white"
                  : "border-line text-navy/60 bg-white hover:border-navy/30 hover:text-navy"
              }`}
            >
              {categoryName}
            </button>
          );
        })}
      </div>

      {/* Content Feed */}
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
          description={
            search
              ? "Try a different search term or clear filters."
              : "Be the first to post in this category."
          }
        />
      ) : (
        <div className="space-y-8">
          {recommended.length > 0 && (
            <section className="space-y-3">
              <p className="text-xs font-medium text-muted">Recommended for you</p>
              <div className="grid sm:grid-cols-2 gap-5">
                {recommended.map((item) => (
                  <ContentCard key={item.id ?? item.ContentID} item={item} />
                ))}
              </div>
            </section>
          )}
          <section className="space-y-3">
            <div className="grid sm:grid-cols-2 gap-5">
              {feedItems.map((item) => (
                <ContentCard key={item.id ?? item.ContentID} item={item} />
              ))}
            </div>
          </section>
        </div>
      )}
    </div>
  );
}
