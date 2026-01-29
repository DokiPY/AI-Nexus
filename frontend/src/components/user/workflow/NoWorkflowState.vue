<template>
  <div class="no-workflow">
    <div class="no-workflow-header">
      <div class="no-workflow-header-left">
        <strong class="no-workflow-title">Workflow</strong>
        <span class="no-workflow-badge">● 不可用</span>
      </div>
    </div>

    <div class="no-workflow-body">
      <div class="no-workflow-content">
        <div class="no-workflow-icon">🚫</div>
        <h2>暂无可用 Workflow</h2>
        <p>请联系管理员开通 Workflow 权限</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.no-workflow {
  width: 100%;
  height: 100%;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  box-shadow: 0 8px 24px rgba(17, 24, 39, 0.06);
  display: flex;
  flex-direction: column;
  margin-top: 12px;
  border-radius: 14px;
}

.no-workflow-header {
  padding: 14px 16px;
  border-bottom: 1px solid #e5e7eb;
  border-radius: 14px 14px 0 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 15px;
  background: #ffffff;
}

.no-workflow-header-left {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.no-workflow-title {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.no-workflow-badge {
  color: #ef4444;
  font-size: 12px;
  font-weight: 500;
}

.no-workflow-body {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 40px;
}

.no-workflow-content {
  text-align: center;
}

.no-workflow-icon {
  font-size: 80px;
  margin-bottom: 24px;
}

.no-workflow-content h2 {
  font-size: 28px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 16px;
}

.no-workflow-content p {
  font-size: 16px;
  color: #6b7280;
  margin: 0;
}
</style>
