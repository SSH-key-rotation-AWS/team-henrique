#!/usr/bin/bash
  sudo sed -i "s/#\$nrconf{kernelhints} = -1;/\$nrconf{kernelhints} = -1;/g" /etc/needrestart/needrestart.conf
  sudo sed -i 's/#$nrconf{restart} = '"'"'i'"'"';/$nrconf{restart} = '"'"'a'"'"';/g' /etc/needrestart/needrestart.conf
  sudo apt update && sudo apt -y upgrade
  sudo apt install python3.11 -y
  curl -sSL https://install.python-poetry.org | python3.11 -
  poetry self add poetry-git-version-plugin
  sudo apt -y install openjdk-11-jdk
  sudo apt -y install nodejs
  sudo apt -y install npm
  npm install octokit
  curl -OL http://mirrors.jenkins-ci.org/war/latest/jenkins.war
  nohup java -jar -Djenkins.install.runSetupWizard=false jenkins.war &
  url="http://localhost:8080"
  while [ "$(curl -s -o /dev/null -w "%{http_code}" $url)" != "200" ]; do sleep 1; done
  wget $url/jnlpJars/jenkins-cli.jar
  touch setup.groovy
  echo "import jenkins.model.*
  import hudson.security.*

  def instance = Jenkins.getInstance()

  def hudsonRealm = new HudsonPrivateSecurityRealm(false)
  hudsonRealm.createAccount(\"TeamHenrique\", \"AWS_SSH\")
  instance.setSecurityRealm(hudsonRealm)
  instance.save()

  def strategy = new hudson.security.FullControlOnceLoggedInAuthorizationStrategy()
  strategy.setAllowAnonymousRead(false)
  instance.setAuthorizationStrategy(strategy)" >> setup.groovy
  java -jar jenkins-cli.jar -s $url groovy = < setup.groovy
  #something goes wrong here
  java -jar jenkins-cli.jar -s $url -auth "TeamHenrique":"AWS_SSH" install-plugin github-branch-source workflow-multibranch multibranch-action-triggers config-file-provider \
    branch-api cloudbees-folder credentials -restart
  touch github_credentials.xml
  echo "<com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl plugin=\"credentials@1254.vb_96f366e7b_a_d\">
  <scope>SYSTEM</scope>
  <id>github_login</id>
  <description></description>
  <username>akrakauer</username>
  <password>
   AQAAABAAAAAQ8zpk4NIt5/Y65bEzbfp2UO9YUMI+zNNPJ6TM/OX6rMM=
  </password>
  <usernameSecret>true</usernameSecret>
</com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl>" >> github_credentials.xml
  java -jar jenkins-cli.jar -s $url -auth "TeamHenrique":"AWS_SSH" create-credentials-by-xml  system::system::jenkins _ < github_credentials.xml
  touch config.xml
  echo "<?xml version='1.1' encoding='UTF-8'?>
<org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject plugin=\"workflow-multibranch@756.v891d88f2cd46\">
  <actions/>
  <description></description>
  <displayName>MultiBranch</displayName>
  <properties>
    <org.jenkinsci.plugins.workflow.multibranch.PipelineTriggerProperty plugin=\"multibranch-action-triggers@1.8.6\">
      <createActionJobsToTrigger></createActionJobsToTrigger>
      <deleteActionJobsToTrigger></deleteActionJobsToTrigger>
      <actionJobsToTriggerOnRunDelete></actionJobsToTriggerOnRunDelete>
      <quitePeriod>0</quitePeriod>
      <branchIncludeFilter>*</branchIncludeFilter>
      <branchExcludeFilter></branchExcludeFilter>
      <additionalParameters/>
    </org.jenkinsci.plugins.workflow.multibranch.PipelineTriggerProperty>
    <org.jenkinsci.plugins.configfiles.folder.FolderConfigFileProperty plugin=\"config-file-provider@938.ve2b_8a_591c596\">
      <configs class=\"sorted-set\">
        <comparator class=\"org.jenkinsci.plugins.configfiles.ConfigByIdComparator\"/>
      </configs>
    </org.jenkinsci.plugins.configfiles.folder.FolderConfigFileProperty>
  </properties>
  <folderViews class=\"jenkins.branch.MultiBranchProjectViewHolder\" plugin=\"branch-api@2.1109.vdf225489a_16d\">
    <owner class=\"org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject\" reference=\"../..\"/>
  </folderViews>
  <healthMetrics/>
  <icon class=\"jenkins.branch.MetadataActionFolderIcon" plugin="branch-api@2.1109.vdf225489a_16d\">
    <owner class=\"org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject\" reference=\"../..\"/>
  </icon>
  <orphanedItemStrategy class=\"com.cloudbees.hudson.plugins.folder.computed.DefaultOrphanedItemStrategy\" plugin=\"cloudbees-folder@6.815.v0dd5a_cb_40e0e\">
    <pruneDeadBranches>false</pruneDeadBranches>
    <daysToKeep>-1</daysToKeep>
    <numToKeep>-1</numToKeep>
    <abortBuilds>false</abortBuilds>
  </orphanedItemStrategy>
  <triggers/>
  <disabled>false</disabled>
  <sources class=\"jenkins.branch.MultiBranchProject\$BranchSourceList\" plugin=\"branch-api@2.1109.vdf225489a_16d\">
    <data>
      <jenkins.branch.BranchSource>
        <source class=\"org.jenkinsci.plugins.github_branch_source.GitHubSCMSource\" plugin=\"github-branch-source@1728.v859147241f49\">
          <id>d6f1f5bc-bbf7-4241-ada7-a8aa7a8877e9</id>
          <apiUri>https://api.github.com</apiUri>
          <credentialsId>github_login</credentialsId>
          <repoOwner>SSH-key-rotation-AWS</repoOwner>
          <repository>team-henrique</repository>
          <repositoryUrl>https://github.com/SSH-key-rotation-AWS/team-henrique</repositoryUrl>
          <traits>
            <org.jenkinsci.plugins.github__branch__source.BranchDiscoveryTrait>
              <strategyId>3</strategyId>
            </org.jenkinsci.plugins.github__branch__source.BranchDiscoveryTrait>
          </traits>
        </source>
        <strategy class=\"jenkins.branch.NamedExceptionsBranchPropertyStrategy\">
          <defaultProperties class=\"empty-list\"/>
          <namedExceptions class=\"empty-list\"/>
        </strategy>
      </jenkins.branch.BranchSource>
    </data>
    <owner class=\"org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject\" reference=\"../..\"/>
  </sources>
  <factory class=\"org.jenkinsci.plugins.workflow.multibranch.WorkflowBranchProjectFactory\">
    <owner class=\"org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject\" reference=\"../..\"/>
    <scriptPath>Jenkinsfile</scriptPath>
  </factory>
</org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject>" >> config.xml
   java -jar jenkins-cli.jar -s $url -auth "TeamHenrique":"AWS_SSH" create-job MultiBranch < config.xml
