export type TabId = 'original' | 'anonymized' | 'replacements' | 'risk' | 'insights';

interface Tab {
  id: TabId;
  label: string;
}

interface TabsProps {
  activeTab: TabId;
  onTabChange: (tab: TabId) => void;
}

const tabs: Tab[] = [
  { id: 'original', label: 'Original Text' },
  { id: 'anonymized', label: 'Anonymized Text' },
  { id: 'replacements', label: 'Replacements' },
  { id: 'risk', label: 'Risk Assessment' },
  { id: 'insights', label: 'Insights' }
];

export function Tabs({ activeTab, onTabChange }: TabsProps) {
  return (
    <div className="tabs" role="tablist">
      {tabs.map(tab => (
        <button
          key={tab.id}
          className={`tab ${activeTab === tab.id ? 'active' : ''}`}
          onClick={() => onTabChange(tab.id)}
          aria-selected={activeTab === tab.id}
          role="tab"
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}
