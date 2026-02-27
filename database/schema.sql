-- Tasks table
CREATE TABLE IF NOT EXISTS tasks (
    task_id TEXT PRIMARY KEY,
    subject TEXT NOT NULL,  -- 语文/数学/英语
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    target_date DATE,
    status TEXT DEFAULT '进行中',  -- 进行中/已完成
    notes TEXT
);

-- Knowledge points table
CREATE TABLE IF NOT EXISTS knowledge_points (
    kp_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    content TEXT NOT NULL,
    type TEXT NOT NULL,  -- 生词/古诗/公式/单词等
    error_count INTEGER DEFAULT 0,
    correct_count INTEGER DEFAULT 0,
    mastery_level TEXT DEFAULT '未测试',  -- 未测试/学习中/需加强/已掌握
    next_review_date DATE,
    last_test_date TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id)
);

-- Learning history table
CREATE TABLE IF NOT EXISTS learning_history (
    record_id TEXT PRIMARY KEY,
    kp_id TEXT NOT NULL,
    test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    result TEXT NOT NULL,  -- 正确/错误
    parent_feedback TEXT,
    agent_response TEXT,
    FOREIGN KEY (kp_id) REFERENCES knowledge_points(kp_id)
);

-- Teaching strategies table
CREATE TABLE IF NOT EXISTS teaching_strategies (
    strategy_id TEXT PRIMARY KEY,
    kp_id TEXT NOT NULL,
    strategy_type TEXT NOT NULL,  -- 记忆口诀/联想记忆/对比学习等
    content TEXT NOT NULL,
    used_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    effectiveness TEXT DEFAULT '未知',  -- 有效/无效/未知
    FOREIGN KEY (kp_id) REFERENCES knowledge_points(kp_id)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_tasks_subject ON tasks(subject);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_kp_task_id ON knowledge_points(task_id);
CREATE INDEX IF NOT EXISTS idx_kp_mastery_level ON knowledge_points(mastery_level);
CREATE INDEX IF NOT EXISTS idx_kp_next_review ON knowledge_points(next_review_date);
CREATE INDEX IF NOT EXISTS idx_history_kp_id ON learning_history(kp_id);
CREATE INDEX IF NOT EXISTS idx_history_test_date ON learning_history(test_date);
CREATE INDEX IF NOT EXISTS idx_strategies_kp_id ON teaching_strategies(kp_id);
